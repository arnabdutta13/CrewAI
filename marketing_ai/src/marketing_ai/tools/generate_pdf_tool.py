import os
from fpdf import FPDF, XPos, YPos, FontFace
import json
from crewai.tools import BaseTool
from datetime import datetime

class GeneratePDFTool(BaseTool):
    name: str = "Generate a PDF Report"
    description: str = "Generates a PDF report from the provided marketing campaign data."

    def _run(self, jsonFilePath: str, outputFilePath: str = None) -> str:
        """
        Generates a PDF report from the provided marketing campaign data.

        Args:
            jsonFilePath (str): The path of the generated campaign.json file.
            outputFilePath (str, optional): The path where the PDF report will be saved. Defaults to None.

        Returns:
            str: The file path of the generated PDF report.
        """
        try:
            if not outputFilePath:
                outputFilePath = os.path.join(os.getcwd(), "campaign.pdf")
            
            with open(jsonFilePath, 'r') as file:
                data = json.load(file)
            
            currentTimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_font("FreeSerif", "", os.path.join(os.getcwd(), "FreeSerif.ttf"))
            pdf.add_font("FreeSerif", "B", os.path.join(os.getcwd(), "FreeSerifBold.ttf"))
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("FreeSerif", "B", 24)

            pdf.cell(0, 20, text="Marketing Campaign Report",new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            pdf.ln(10)

            pdf.set_font("FreeSerif", "B", 12)
            pdf.cell(0, 10, text=f"Generated on: {currentTimestamp}",new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            
            effective_page_width = pdf.w - 2*pdf.l_margin
            for campaign in data['campaigns']:
                pdf.add_page()

                data = (
                            ("Campaign Name",  campaign['name']),
                            ("Objective", campaign['objective']),
                            ("Target Audience", campaign['target_audience']),
                            ("Campaign Details", campaign.get('campaign_details')),
                            ("Strategy Score", campaign['strategy']['score']),
                            ("Trending Topics", ", ".join([topic['name'] for topic in campaign['strategy']['topics']['topics']])),
                    )
                
                with pdf.table(col_widths=(50, 100)) as table:
                    for data_row in data:
                        row = table.row()
                        pdf.set_fill_color(200, 200, 255)
                        pdf.set_font("FreeSerif", "B", 10)
                        row.cell(text=data_row[0], align='L')
                        pdf.set_fill_color(255, 255, 255)
                        pdf.set_font("FreeSerif", "", 10)
                        row.cell(text=data_row[1], align='L')
                
            pdf.output(outputFilePath)
            print (f"PDF report generated successfully: {os.path.abspath(outputFilePath)}")
            return f"PDF report generated successfully: {os.path.abspath(outputFilePath)}"
        except Exception as e:
            print(f"Error generating PDF: {e}")
            raise e
        
#tool = GeneratePDFTool()
#tool._run("output/campaigns.json")  # Example usage