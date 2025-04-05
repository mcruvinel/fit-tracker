from fpdf import FPDF
from datetime import datetime
from typing import Dict, Any
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class PDFReportGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
    
    def generate_report(self, workout_data: Dict[str, Any]) -> bytes:
        self.pdf.add_page()
        self._add_header(workout_data)
        self._add_summary(workout_data)
        self._add_charts(workout_data)
        self._add_raw_data(workout_data)
        return self.pdf.output(dest='S').encode('latin1')

    def _add_header(self, data: Dict[str, Any]):
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, f"Relatório de Atividade - {data['sport']}", 0, 1, 'C')
        self.pdf.ln(5)

    def _add_summary(self, data: Dict[str, Any]):
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, 'Resumo da Atividade', 0, 1)
        self.pdf.set_font('Arial', '', 10)
        
        summary = [
            f"Data: {data['start_time']}",
            f"Distância: {data['total_distance'] / 1000:.2f} km",
            f"Duração: {datetime(seconds=data['total_elapsed_time'])}",
            f"FC Média: {data.get('avg_heart_rate', 'N/A')} bpm"
        ]
        
        for line in summary:
            self.pdf.cell(0, 10, line, 0, 1)

    def _add_charts(self, data: Dict[str, Any]):
        if 'records' not in data:
            return
            
        df = data['records']
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, 'Gráficos de Performance', 0, 1)
        
        # Gráfico de FC
        if 'heart_rate' in df.columns:
            plt.figure()
            df['heart_rate'].plot(title='Frequência Cardíaca')
            self._insert_plot()

    def _insert_plot(self):
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img = base64.b64encode(buf.getvalue()).decode('latin1')
        self.pdf.image(BytesIO(base64.b64decode(img)), x=10, w=190)
        self.pdf.ln(5)

    def _add_raw_data(self, data: Dict[str, Any]):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, 'Dados Brutos', 0, 1)
        self.pdf.set_font('Courier', '', 8)
        
        if 'records' in data:
            for _, row in data['records'].iterrows():
                self.pdf.cell(0, 5, str(row.to_dict()), 0, 1)