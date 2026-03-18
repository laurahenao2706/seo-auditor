"""
Script para convertir el reporte Markdown a HTML con estilos profesionales
"""

import markdown
from pathlib import Path

# Leer el archivo Markdown
md_path = Path(__file__).parent / "REPORTE_TECNICO_DETALLADO.md"
html_path = Path(__file__).parent / "REPORTE_TECNICO_DETALLADO.html"

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convertir a HTML con extensiones
html_body = markdown.markdown(
    md_content,
    extensions=[
        'tables',           # Soporte para tablas
        'fenced_code',      # Bloques de código con ```
        'toc',              # Tabla de contenidos
        'sane_lists',       # Listas mejoradas
        'nl2br',            # Saltos de línea
    ]
)

# Template HTML con estilos profesionales
html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Técnico Detallado - SEO Auditor</title>
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
            --bg-color: #f8f9fa;
            --code-bg: #f4f4f4;
            --border-color: #dee2e6;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: var(--bg-color);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: var(--primary-color);
            font-size: 2.5em;
            margin-bottom: 0.5em;
            padding-bottom: 0.3em;
            border-bottom: 3px solid var(--secondary-color);
        }}
        
        h2 {{
            color: var(--primary-color);
            font-size: 2em;
            margin-top: 1.5em;
            margin-bottom: 0.7em;
            padding-left: 10px;
            border-left: 4px solid var(--secondary-color);
        }}
        
        h3 {{
            color: var(--secondary-color);
            font-size: 1.5em;
            margin-top: 1.2em;
            margin-bottom: 0.5em;
        }}
        
        h4 {{
            color: #555;
            font-size: 1.2em;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }}
        
        p {{
            margin-bottom: 1em;
            text-align: justify;
        }}
        
        /* Tablas */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            overflow: hidden;
            border-radius: 8px;
        }}
        
        th {{
            background-color: var(--primary-color);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid var(--border-color);
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tr:hover {{
            background-color: #e9ecef;
            transition: background-color 0.3s ease;
        }}
        
        /* Código */
        code {{
            background-color: var(--code-bg);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            color: #c7254e;
        }}
        
        pre {{
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 1em 0;
            border-left: 4px solid var(--secondary-color);
        }}
        
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
            font-size: 0.95em;
        }}
        
        /* Listas */
        ul, ol {{
            margin-left: 2em;
            margin-bottom: 1em;
        }}
        
        li {{
            margin-bottom: 0.5em;
        }}
        
        /* Blockquotes */
        blockquote {{
            border-left: 4px solid var(--secondary-color);
            padding-left: 20px;
            margin: 1em 0;
            color: #666;
            font-style: italic;
            background-color: #f9f9f9;
            padding: 15px 20px;
            border-radius: 0 5px 5px 0;
        }}
        
        /* Links */
        a {{
            color: var(--secondary-color);
            text-decoration: none;
            border-bottom: 1px dotted var(--secondary-color);
        }}
        
        a:hover {{
            color: var(--primary-color);
            border-bottom: 1px solid var(--primary-color);
        }}
        
        /* Badges y highlights */
        strong {{
            color: var(--primary-color);
            font-weight: 600;
        }}
        
        /* Símbolos especiales */
        .emoji {{
            font-size: 1.2em;
        }}
        
        /* Separadores */
        hr {{
            border: none;
            border-top: 2px solid var(--border-color);
            margin: 2em 0;
        }}
        
        /* Cajas de información */
        .info-box {{
            background-color: #e7f3ff;
            border-left: 4px solid var(--secondary-color);
            padding: 15px;
            margin: 1em 0;
            border-radius: 0 5px 5px 0;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            h2 {{
                font-size: 1.5em;
            }}
            
            table {{
                font-size: 0.9em;
            }}
            
            th, td {{
                padding: 8px;
            }}
        }}
        
        /* Print styles */
        @media print {{
            body {{
                background: white;
            }}
            
            .container {{
                box-shadow: none;
                padding: 0;
            }}
            
            h1, h2 {{
                page-break-after: avoid;
            }}
            
            table, pre {{
                page-break-inside: avoid;
            }}
        }}
        
        /* Tabla de contenidos */
        .toc {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 2em 0;
            border: 1px solid var(--border-color);
        }}
        
        .toc ul {{
            list-style: none;
            margin-left: 0;
        }}
        
        .toc li {{
            margin-bottom: 0.3em;
        }}
        
        /* Checklist items */
        li:has(> input[type="checkbox"]) {{
            list-style: none;
            margin-left: -1.5em;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
    </div>
    
    <script>
        // Smooth scrolling para links internos
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});
        
        // Highlight de código
        document.querySelectorAll('pre code').forEach((block) => {{
            // Agregar números de línea
            const lines = block.textContent.split('\\n');
            if (lines.length > 3) {{
                block.innerHTML = lines.map((line, i) => 
                    `<span style="color: #6c757d; user-select: none; padding-right: 1em;">${{(i + 1).toString().padStart(2, ' ')}}</span>${{line}}`
                ).join('\\n');
            }}
        }});
    </script>
</body>
</html>
"""

# Guardar el HTML
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"✅ HTML generado exitosamente en: {html_path}")
print(f"📂 Abre el archivo en tu navegador para ver el reporte formateado")
