import csv

class CSVCleaner:
    def __init__(self, delimiter=';'):
        self.delimiter = delimiter

    def clean_csv(self, input_file, output_file):
        # Read the header row to get the column names
        with open(input_file, 'r') as infile:
            reader = csv.reader(infile, delimiter=self.delimiter)
            header = next(reader)  # Read the header row
            num_columns = len(header)

        # Create an output file and start processing the rows
        with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.reader(infile, delimiter=self.delimiter)
            writer = csv.writer(outfile, delimiter=self.delimiter)

            # Write the header to the output file
            writer.writerow(header)

            for row in reader:
                if len(row) == num_columns:
                    # Row is correct, write it to the output
                    writer.writerow(row)
                elif len(row) > num_columns:
                    # Too many columns, try to merge extra columns
                    corrected_row = row[:num_columns-1] + [self.delimiter.join(row[num_columns-1:])]
                    writer.writerow(corrected_row)
                elif len(row) < num_columns:
                    # Too few columns, pad with empty strings or drop the line
                    row += [''] * (num_columns - len(row))
                    writer.writerow(row)

        return header  # Return the column names for later use