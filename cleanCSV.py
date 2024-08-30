import csv

def clean_csv(input_file, output_file):
    # Determine the expected number of columns
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header row
        num_columns = len(header)
    
    # Create an output file and start processing the rows
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write the header to the output file
        writer.writerow(header)
        
        for row in reader:
            if len(row) == num_columns:
                # Row is correct, write it to the output
                writer.writerow(row)
            elif len(row) > num_columns:
                # Too many columns, try to merge extra columns
                corrected_row = row[:num_columns-1] + [','.join(row[num_columns-1:])]
                writer.writerow(corrected_row)
            elif len(row) < num_columns:
                # Too few columns, pad with empty strings or drop the line
                row += [''] * (num_columns - len(row))
                writer.writerow(row)

# Usage
input_file = 'table1.csv'
output_file = 'cleaned_table1.csv'
clean_csv(input_file, output_file)