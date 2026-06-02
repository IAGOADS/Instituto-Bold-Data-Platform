# utils/pdf_service.py
import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Definição da Paleta de Cores Institucionais
COLOR_PURPLE = colors.HexColor("#522f8b")
COLOR_GOLD = colors.HexColor("#fb9e21")
COLOR_BLUE = colors.HexColor("#004B87")
COLOR_DARK = colors.HexColor("#0c2340")
COLOR_LIGHT = colors.HexColor("#f8f9fa")
COLOR_GREY = colors.HexColor("#6c757d")

def generate_pdf_report(df, kpis, inclusion_index, vulnerability_index, transformation_potential, insights):
    """
    Gera um relatório PDF executivo premium usando ReportLab e retorna como um buffer de bytes.
    Reflete dinamicamente os dados filtrados (ex: Mulheres, Uberlândia, Baixa Renda).
    """
    buffer = io.BytesIO()
    
    # Configuração da página
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # --- ESTILOS CUSTOMIZADOS ---
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=COLOR_PURPLE,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=COLOR_BLUE,
        spaceAfter=15
    )
    
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        textColor=COLOR_DARK,
        spaceBefore=14,
        spaceAfter=8,
        borderColor=COLOR_PURPLE,
        borderWidth=1,
        borderPadding=4
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        spaceAfter=6
    )
    
    kpi_title_style = ParagraphStyle(
        'KPITitle',
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=COLOR_GREY,
        alignment=1 # Centralizado
    )
    
    kpi_val_style = ParagraphStyle(
        'KPIVal',
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=COLOR_PURPLE,
        alignment=1 # Centralizado
    )
    
    insight_style = ParagraphStyle(
        'InsightStyle',
        fontName='Helvetica',
        fontSize=9.5,
        textColor=colors.HexColor("#444444"),
        leftIndent=15,
        spaceAfter=8
    )
    
    # --- BANNER DO CABEÇALHO ---
    header_data = [
        [
            Paragraph("<b>INSTITUTO BOLD</b>", ParagraphStyle('BoldL', fontName='Helvetica-Bold', fontSize=18, textColor=COLOR_PURPLE)),
            Paragraph("<b>ADM (Archer Daniels Midland)</b>", ParagraphStyle('AdmL', fontName='Helvetica-Bold', fontSize=14, textColor=COLOR_BLUE, alignment=2))
        ]
    ]
    header_table = Table(header_data, colWidths=[3.5*inch, 4.0*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (-1,-1), 2, COLOR_GOLD)
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))
    
    # --- TÍTULO ---
    story.append(Paragraph("Relatório Executivo de Impacto Social", title_style))
    story.append(Paragraph("Demonstração de Diversidade, Inclusão e Empregabilidade do Programa", subtitle_style))
    
    # --- TABELA DE KPIs ---
    kpi_data = [
        [
            Paragraph("TOTAL INSCRITOS", kpi_title_style),
            Paragraph("TOTAL APROVADOS", kpi_title_style),
            Paragraph("TAXA APROVAÇÃO", kpi_title_style),
            Paragraph("CIDADES IMPACTADAS", kpi_title_style)
        ],
        [
            Paragraph(f"{kpis['total_inscritos']}", kpi_val_style),
            Paragraph(f"{kpis['total_aprovados']}", kpi_val_style),
            Paragraph(f"{kpis['taxa_aprovacao']:.1f}%", kpi_val_style),
            Paragraph(f"{kpis['cidades_impactadas']}", kpi_val_style)
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[1.87*inch, 1.87*inch, 1.87*inch, 1.87*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_LIGHT),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e9ecef")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e9ecef")),
        ('LINEBELOW', (0,0), (-1,0), 1.5, COLOR_BLUE)
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 15))
    
    # --- MÉTRICAS ESG ---
    story.append(Paragraph("Indicadores Estratégicos de Impacto (D&I e ESG)", section_title))
    esg_data = [
        [
            Paragraph("<b>Métrica Executiva</b>", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<b>Resultado</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, alignment=1)),
            Paragraph("<b>Finalidade Estratégica</b>", ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))
        ],
        [
            Paragraph("<b>Índice de Inclusão (D&I)</b>", ParagraphStyle('Eb1', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_DARK)),
            Paragraph(f"<b>{inclusion_index:.1f}%</b>", ParagraphStyle('Eb2', fontName='Helvetica-Bold', fontSize=11, textColor=COLOR_PURPLE, alignment=1)),
            Paragraph("Percentual de participantes das categorias sub-representadas: mulheres, minorias étnico-raciais, PCDs e baixa renda.", ParagraphStyle('Eb3', fontSize=8.5))
        ],
        [
            Paragraph("<b>Índice de Vulnerabilidade Social</b>", ParagraphStyle('Eb4', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_DARK)),
            Paragraph(f"<b>{vulnerability_index:.1f}%</b>", ParagraphStyle('Eb5', fontName='Helvetica-Bold', fontSize=11, textColor=COLOR_BLUE, alignment=1)),
            Paragraph("Proporção de participantes expostos a acentuadas barreiras socioeconômicas (cumulativo de desemprego e baixíssima renda).", ParagraphStyle('Eb6', fontSize=8.5))
        ],
        [
            Paragraph("<b>Potencial de Transformação</b>", ParagraphStyle('Eb7', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_DARK)),
            Paragraph(f"<b>{transformation_potential:.1f}%</b>", ParagraphStyle('Eb8', fontName='Helvetica-Bold', fontSize=11, textColor=COLOR_GOLD, alignment=1)),
            Paragraph("Representa o potencial de mudança social gerado pela formação em jovens desempregados e em busca do 1º emprego.", ParagraphStyle('Eb9', fontSize=8.5))
        ]
    ]
    esg_table = Table(esg_data, colWidths=[2.2*inch, 1.2*inch, 4.1*inch])
    esg_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PURPLE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('LINEBELOW', (0,0), (-1,0), 2, COLOR_GOLD)
    ]))
    story.append(esg_table)
    story.append(Spacer(1, 15))
    
    # --- STORYTELLING E INSIGHTS ---
    story.append(Paragraph("Storytelling de Resultados & Insights Executivos", section_title))
    
    insight_story = []
    for insight in insights:
        # Limpa tags HTML para o PDF e substitui pelo padrão ReportLab
        clean_insight = insight.replace("<strong>", "<b>").replace("</strong>", "</b>")
        insight_story.append(Paragraph(f"• {clean_insight}", insight_style))
        insight_story.append(Spacer(1, 3))
        
    story.append(KeepTogether(insight_story))
    story.append(Spacer(1, 12))
    
    # --- PERFIL SOCIODEMOGRÁFICO ---
    story.append(Paragraph("Perfil Sociodemográfico e Educacional (Resumo)", section_title))
    
    # Cálculos dinâmicos a partir do dataframe (já refletindo os filtros da página principal)
    total_linhas = len(df)
    genero_f = (len(df[df["genero"] == "Feminino"]) / total_linhas) * 100 if total_linhas > 0 else 0
    baixa_r = (len(df[df["renda_familiar"].isin(["Até 1 salário mínimo", "De 1 a 2 salários mínimos"])]) / total_linhas) * 100 if total_linhas > 0 else 0
    negros = (len(df[df["grupo_etnico"].isin(["Preta", "Parda"])]) / total_linhas) * 100 if total_linhas > 0 else 0
    pcd_p = (len(df[df["pcd"] == "Sim"]) / total_linhas) * 100 if total_linhas > 0 else 0
    desemp_p = (len(df[df["empregabilidade"] == "Desempregado"]) / total_linhas) * 100 if total_linhas > 0 else 0
    
    profile_data = [
        [
            Paragraph("<b>Dimensão Socioeconômica</b>", ParagraphStyle('P1', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<b>Proporção do Público Aprovado/Filtrado</b>", ParagraphStyle('P2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, alignment=1))
        ],
        [
            Paragraph("Representatividade Feminina (Equidade de Gênero)", body_style),
            Paragraph(f"<b>{genero_f:.1f}%</b>", ParagraphStyle('V1', fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_PURPLE, alignment=1))
        ],
        [
            Paragraph("Representatividade Étnico-Racial (Pretos e Pardos)", body_style),
            Paragraph(f"<b>{negros:.1f}%</b>", ParagraphStyle('V2', fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_BLUE, alignment=1))
        ],
        [
            Paragraph("Vulnerabilidade de Renda (Renda familiar <= 2 salários mínimos)", body_style),
            Paragraph(f"<b>{baixa_r:.1f}%</b>", ParagraphStyle('V3', fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_GOLD, alignment=1))
        ],
        [
            Paragraph("Inclusão de Pessoas com Deficiência (PCD)", body_style),
            Paragraph(f"<b>{pcd_p:.1f}%</b>", ParagraphStyle('V4', fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_DARK, alignment=1))
        ],
        [
            Paragraph("Nível de Desemprego (Momento da Inscrição)", body_style),
            Paragraph(f"<b>{desemp_p:.1f}%</b>", ParagraphStyle('V5', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#dc3545"), alignment=1))
        ]
    ]
    
    profile_table = Table(profile_data, colWidths=[4.7*inch, 2.8*inch])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_BLUE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('LINEBELOW', (0,0), (-1,0), 2, COLOR_GOLD)
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 20))
    
    # --- RODAPÉ ---
    footer_text = Paragraph(
        "<font color='#6c757d'>Relatório gerado automaticamente em "
        + datetime.now().strftime("%d/%m/%Y às %H:%M")
        + ". Todos os direitos reservados ao Instituto Bold e ADM.</font>",
        ParagraphStyle('Footer', fontName='Helvetica-Oblique', fontSize=8, alignment=1)
    )
    story.append(footer_text)
    
    # Constrói o PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer.getvalue()