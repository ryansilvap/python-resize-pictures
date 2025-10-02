# ============================================================================
# CÓDIGO MELHORADO - COMPACTADOR DE IMAGENS
# ============================================================================

import os
import logging
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image
import jinja2
import pdfkit
from typing import List, Dict, Tuple


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

class Config:
    """Configurações centralizadas do sistema"""
    FOLDER_PATH = r'Z:\Segurança'
    MIN_FILE_SIZE_KB = 2000  # Processar apenas arquivos > 2MB
    QUALITY = 85  # Qualidade JPEG (0-100)
    MAX_DIMENSION = 1920  # Redimensionar se maior que isso
    VALID_EXTENSIONS = ['.jpg', '.jpeg']
    WKHTMLTOPDF_PATH = r"C:\wkhtmltox\bin\wkhtmltopdf.exe"

    # Template HTML melhorado
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .info { margin-bottom: 20px; }
            .title { margin-bottom: 0px; padding-bottom: 0px; }
            .underline { text-decoration: underline; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }
            th { background-color: #f2f2f2; font-weight: bold; }
            .savings-positive { color: #28a745; font-weight: bold; }
            .savings-negative { color: #dc3545; font-weight: bold; }
            .summary { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>MINASLIGAS S.A.</h1>
            <h2>Relatório de Compactação de Imagens</h2>
        </div>

        <div class="info">
            <p><strong>Diretório:</strong> {{ folder_path }}</p>
            <p><strong>Data de Processamento:</strong> {{ date }}</p>
            <p><strong>Total de Imagens Processadas:</strong> {{ total_processed }}</p>
        </div>
        
        <div class="summary">
            <h3 class="underline">Resumo</h3>
            <p><strong>Espaço Total Economizado:</strong> {{ "%.2f"|format(total_savings) }} MB</p>
            <p><strong>Economia Média:</strong> {{ "%.1f"|format(average_savings) }}%</p>
            <p><strong>Maior Economia:</strong> {{ "%.1f"|format(max_savings) }}%</p>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Nº</th>
                    <th>Imagem Original</th>
                    <th>Tamanho Original (MB)</th>
                    <th>Tamanho Final (MB)</th>
                    <th>Economia (%)</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for item in processed_files %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ item.original_name }}</td>
                    <td>{{ "%.2f"|format(item.original_size) }}</td>
                    <td>{{ "%.2f"|format(item.final_size) }}</td>
                    <td class="{{ 'savings-positive' if item.savings > 0 else 'savings-negative' }}">
                        {{ "%.1f"|format(item.savings) }}%
                    </td>
                    <td>{{ item.status }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

    </body>
    </html>
    """


# ============================================================================
# CLASSE PRINCIPAL
# ============================================================================

class ImageCompressor:
    """Classe principal para compactação de imagens"""

    def __init__(self):
        self.processed_files: List[Dict] = []
        self.setup_logging()

    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('image_compressor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def is_valid_image(self, file_path: Path) -> bool:
        """Verifica se o arquivo é uma imagem válida para processar"""
        try:
            if file_path.suffix.lower() not in Config.VALID_EXTENSIONS:
                return False

            if file_path.name == 'Thumbs.db':
                return False

            if not file_path.exists():
                return False

            file_size_kb = file_path.stat().st_size / 1024
            if file_size_kb <= Config.MIN_FILE_SIZE_KB:
                return False

            # Tenta abrir a imagem para verificar se não está corrompida
            with Image.open(file_path) as img:
                img.verify()

            return True

        except Exception as e:
            self.logger.warning(f"Arquivo inválido {file_path}: {e}")
            return False

    def compress_image(self, file_path: Path) -> Tuple[bool, str, float, float]:
        """
        Compacta uma imagem individual
        Returns: (success, status_message, original_size_mb, final_size_mb)
        """
        try:
            original_size = file_path.stat().st_size / (1024 * 1024)  # MB

            # Criar nome temporário
            temp_name = file_path.stem + "_compressed" + file_path.suffix
            temp_path = file_path.parent / temp_name

            with Image.open(file_path) as image:
                # Converter para RGB se necessário (para JPEG)
                if image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')

                # Redimensionar se muito grande
                if image.width > Config.MAX_DIMENSION or image.height > Config.MAX_DIMENSION:
                    image.thumbnail((Config.MAX_DIMENSION, Config.MAX_DIMENSION), Image.LANCZOS)
                    self.logger.info(f"Redimensionado: {file_path.name}")

                # Salvar com compactação
                image.save(
                    temp_path,
                    quality=Config.QUALITY,
                    optimize=True,
                    format='JPEG'
                )

            # Verificar se houve economia
            final_size = temp_path.stat().st_size / (1024 * 1024)  # MB

            if final_size < original_size:
                # Substituir arquivo original
                shutil.copystat(file_path, temp_path)
                file_path.unlink()  # Remove original
                temp_path.rename(file_path)  # Renomeia temp para original

                self.logger.info(f"Compactado: {file_path.name} ({original_size:.2f}MB → {final_size:.2f}MB)")
                return True, "Compactado com sucesso", original_size, final_size
            else:
                # Remove arquivo temporário se não houve melhoria
                temp_path.unlink()
                self.logger.info(f"Sem melhoria: {file_path.name}")
                return False, "Sem melhoria possível", original_size, original_size

        except Exception as e:
            self.logger.error(f"Erro ao compactar {file_path}: {e}")
            # Limpar arquivo temporário se existir
            temp_path = file_path.parent / (file_path.stem + "_compressed" + file_path.suffix)
            if temp_path.exists():
                temp_path.unlink()
            return False, f"Erro: {str(e)}", 0, 0

    def process_folder(self, folder_path: str) -> int:
        """Processa todas as imagens em uma pasta e subpastas"""
        folder = Path(folder_path)
        if not folder.exists():
            self.logger.error(f"Pasta não encontrada: {folder_path}")
            return 0

        self.logger.info(f"Iniciando processamento da pasta: {folder_path}")
        processed_count = 0

        # Buscar todas as imagens recursivamente
        for file_path in folder.rglob("*"):
            if not file_path.is_file():
                continue

            if self.is_valid_image(file_path):
                try:
                    success, status, original_size, final_size = self.compress_image(file_path)

                    # Calcular economia
                    if original_size > 0:
                        savings = ((original_size - final_size) / original_size) * 100
                    else:
                        savings = 0

                    # Adicionar aos resultados
                    self.processed_files.append({
                        'original_name': file_path.name,
                        'path': str(file_path.parent),
                        'original_size': original_size,
                        'final_size': final_size,
                        'savings': savings,
                        'status': status,
                        'success': success
                    })

                    if success:
                        processed_count += 1

                except Exception as e:
                    self.logger.info(f"Erro {e} no arquivo {file_path}")
                    continue

        self.logger.info(f"Processamento concluído. {processed_count} imagens compactadas.")
        return processed_count

    def generate_report(self, folder_path: str) -> str:
        """Gera o relatório PDF consolidado"""
        try:
            if not self.processed_files:
                self.logger.warning("Nenhum arquivo foi processado para gerar relatório")
                return ""

            # Calcular estatísticas
            successful_files = [f for f in self.processed_files if f['success']]
            total_savings_mb = sum(f['original_size'] - f['final_size'] for f in successful_files)
            average_savings = sum(f['savings'] for f in successful_files) / len(
                successful_files) if successful_files else 0
            max_savings = max(f['savings'] for f in successful_files) if successful_files else 0

            # Preparar dados para o template
            template_data = {
                'folder_path': folder_path,
                'date': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'processed_files': self.processed_files,
                'total_processed': len(self.processed_files),
                'total_savings': total_savings_mb,
                'average_savings': average_savings,
                'max_savings': max_savings
            }

            # Renderizar HTML
            template = jinja2.Template(Config.HTML_TEMPLATE)
            html_content = template.render(**template_data)

            # Gerar PDF
            report_path = Path(folder_path) / f"relatorio_compactacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            config = pdfkit.configuration(wkhtmltopdf=Config.WKHTMLTOPDF_PATH)
            pdfkit.from_string(
                html_content,
                str(report_path),
                configuration=config,
                options={'page-size': 'A4', 'encoding': 'UTF-8'}
            )

            self.logger.info(f"Relatório gerado: {report_path}")
            return str(report_path)

        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {e}")
            return ""


# ============================================================================
# SCRIPT PRINCIPAL
# ============================================================================

def main():
    """Função principal"""
    print("🖼️  COMPACTADOR DE IMAGENS")
    print("=" * 50)

    # Criar instância do compactador
    compressor = ImageCompressor()

    # Processar imagens
    start_time = datetime.now()
    processed_count = compressor.process_folder(Config.FOLDER_PATH)
    end_time = datetime.now()

    # Gerar relatório
    if processed_count > 0:
        report_path = compressor.generate_report(Config.FOLDER_PATH)

        print(f"\n✅ PROCESSAMENTO CONCLUÍDO!")
        print(f"📊 Imagens processadas: {processed_count}")
        print(f"⏱️  Tempo total: {end_time - start_time}")
        print(f"📄 Relatório: {report_path}")
    else:
        print("\n⚠️  Nenhuma imagem foi processada.")
        print("Verifique se existem imagens válidas na pasta especificada.")


if __name__ == "__main__":
    main()