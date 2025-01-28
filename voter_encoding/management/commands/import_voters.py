import os
import pandas as pd
from django.core.management.base import BaseCommand
from voter_encoding.models import VotersList  # Ensure the model is correct

class Command(BaseCommand):
    help = 'Import voters data from all Excel files in a directory'

    def handle(self, *args, **kwargs):
        # Specify the directory where your Excel files are located
        # Example of absolute path
        folder_path = '/Users/billiedelossantos/Documents/Visual Studio Code/voter_encoding/voter_management/voter_encoding/PCVL/'


        # List all Excel files in the directory
        excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]  # Or use .xls if needed
        print(excel_files)

        # Process each Excel file found in the folder
        for excel_file_name in excel_files:
            excel_file_path = os.path.join(folder_path, excel_file_name)

            # Open and read each Excel file using pandas
            df = pd.read_excel(excel_file_path, engine='openpyxl')  # You may choose different sheetname if needed
            print(f"Processing file: {excel_file_name}")
            print("Excel Headers:", df.columns.tolist())
            print("Barangay: "+ excel_file_name.split('.')[0])
            for index, row in df.iterrows():
                # Clean headers and row values if needed
                precinct = str(row.iloc[0]).strip()  # Column index 0 for PRECINCT
                legend = str(row.iloc[1]).strip() if pd.notnull(row.iloc[1]) else "Regular"  # Column index 1 for LEGEND
                name = str(row.iloc[2]).strip()  # Column index 2 for NAME
                address = str(row.iloc[3]).strip()  # Column index 3 for ADDRESS

                barangay = excel_file_name.split('.')[0]

                # Only insert the row if key fields are not empty
                if precinct and name:  # Custom validation, add further checks if necessary
                    # Create and save the Voter record to the database
                    VotersList.objects.create(
                        precinct_number=precinct,
                        legend=legend or "",  # If legend is missing, insert None
                        name=name,
                        address=address,
                        barangay=barangay
                    )
                else:
                    print(f"Skipping row with missing crucial data in file {excel_file_name}: {row}")

        self.stdout.write(self.style.SUCCESS('Successfully imported all voter data from Excel files.'))
