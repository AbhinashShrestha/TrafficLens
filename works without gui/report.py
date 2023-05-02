import os
from PIL import Image
import pandas as pd
from fpdf import FPDF #pip install fpdf
from main import base_name
# Read the Excel file into a pandas DataFrame

filename = f'overspeeding_vehicles_{base_name}/overspeeding_vehicles.xlsx'
df = pd.read_excel(filename)
class FPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 30)
        self.cell(0, 5, 'VEHICLE REPORT', align="C")
        # Line break
        self.ln(30)
# Initialize a FPDF object
pdf = FPDF('L',"mm","A5")


# Define the column widths and heights
col_widths = [90, 80]
col_height = 80

# Set the font for the PDF
pdf.set_font('Arial', 'B', 16)

# Loop through each row in the DataFrame
for index, row in df.iterrows():

    # Extract the image filename from the Vehicle Type column
    # image_filename = f'overspeeding_vehicles_{base_name}/{}_{}.png'.format(row['Vehicle Type'], row['Vehicle id'])
    image_filename = f'overspeeding_vehicles_{base_name}/{row["Vehicle Type"]}_{row["Vehicle id"]}.png'


    # Check if the image file exists
    if not os.path.exists(image_filename):
        print('Image file not found: {}'.format(image_filename))
        continue

    # Open the image file and resize it to fit the column width
    image = Image.open(image_filename)
    image_width, image_height = image.size
    aspect_ratio = image_width / float(image_height)
    new_height = col_height - 20
    new_width = int(new_height * aspect_ratio)
    image = image.resize((new_width, new_height))

    # Add a new page to the PDF document
    pdf.add_page()

    # Set the x and y positions to start drawing the text
    x = pdf.get_x()
    y = pdf.get_y()

    # pdf.text(x: 30.5, y: 20, txt: "-------------------------------VEHICLE REPORT-------------------------------")
    # Add the Vehicle Type text to the page
    pdf.cell(col_widths[0], col_height/3, f'Vehicle Type: {row["Vehicle Type"]}')
    pdf.ln(15)

    # Add the Vehicle id text to the page
    pdf.cell(col_widths[0], col_height/3, f'Vehicle id: {row["Vehicle id"]}')
    pdf.ln(15)

    # Add the Speed text to the page
    pdf.cell(col_widths[0], col_height/3, f'Speed : {row["Speed (km/hr)"]} km/hr')
    pdf.ln(15)

    # Add the Remarks text to the page
    pdf.cell(col_widths[0], col_height/3, f'Remarks: Exceeded Speed Limit')
    pdf.ln(20)

    # Add the image to the page
    pdf.image(image_filename, x=x+col_widths[0]+30, y=y, w=new_width, h=new_height)

    # Move the y position down for the next row
    pdf.ln(col_height)

# Save the PDF document
pdf.output(f'report_{base_name}.pdf', 'F')


