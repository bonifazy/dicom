from pathlib import Path
from pydicom import dcmread


# source directory with .dcm files
source_dir = 'src'

# file with full filepaths old .dcm file and its matches new file with anonymous PatientName attribute
match = 'match_file.txt'

src_dir = Path(source_dir)

# get only .dcm files from src/ directory
dcm_files = [i for i in src_dir.iterdir() if i.is_file() and i.suffix == '.dcm']

# write statistic of old and new .dcm filepaths
with open(match, 'w') as match_file:

    for dcm_file in dcm_files:
        dcm_file = str(dcm_file)
        ds = dcmread(dcm_file)  # get metadata from .dcm file
        if hasattr(ds, 'PatientName'):
            ds.PatientName = ''  # Clear patient name value if name exist

        # write this dicom file with anonymous PatientName to new directory 
        if hasattr(ds, 'StudyInstanceUID') and hasattr(ds, 'SeriesInstanceUID') and hasattr(ds, 'SOPInstanceUID'):
            path = Path(ds.StudyInstanceUID, ds.SeriesInstanceUID)  # merge attr values to create new paths
            path.mkdir(parents=True, exist_ok=True)  # confirm create this path
            new_dcm_name = ds.SOPInstanceUID + '.dcm'
            new_dcm_file = str(Path(path, new_dcm_name))  # new file with path
            ds.save_as(new_dcm_file)  # create new .dcm file in new directory

        # write line with full paths of old and new dcm files to match_files.txt
        line = dcm_file + '\t' + new_dcm_file + '\n'
        match_file.write(line)
