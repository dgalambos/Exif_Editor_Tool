import csv
import exiftool
import os
import time
from tqdm import tqdm
import argparse
from pprint import pprint
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

rowCount = 1

def init():
    output_path = raw_input("Drag destination folder here: ").strip() + "/"
    csv_filename = raw_input("Designate output CSV filename: ").replace(" ", "_")
    csv_filename = csv_filename.replace(".csv", "")
    csvFile = output_path + csv_filename+".csv"

    file_list = []

    more = "yes"
    while (more == "y" or more == "yes"):
        images_folder = raw_input("Drag asset folder here: ").strip() + "/"
        print "\nThere are " + str(
            len(os.listdir(images_folder))) + " files in this directory..."
        confirmation = raw_input("\nContinue? (Y/N): ").lower()
        if (confirmation == "y" or confirmation == "yes"):
            for file_path in os.listdir(images_folder):
                if (file_path.startswith(".") or file_path.endswith(".csv")):
                    print "Ignored: " + file_path
                    continue
                else:
                    file_path = images_folder + file_path
                    if not os.path.isfile(file_path):
                        print "ERROR: File %s is not valid." % file_path
                        continue
                    else:
                        file_list.append(file_path)
            more = raw_input("Add more assets?: ").lower()
    # pprint(file_list)
    tags = ["Directory",
            "Filename",
            "DateTimeOriginal",
            "GPSLatitude",
            "GPSLatitudeRef",
            "GPSLongitude",
            "GPSLongitudeRef",
            "Subject"]
    metadata = {"File:Directory":"",
                 "File:FileName":"",
                 "EXIF:DateTimeOriginal":"",
                 "EXIF:GPSLatitude":"",
                 "EXIF:GPSLatitudeRef":"",
                 "EXIF:GPSLongitude":"",
                 "EXIF:GPSLongitudeRef":"",
                 "XMP:Subject":""}

    with exiftool.ExifTool() as et:
        with open(csvFile, mode='w') as file:
            writer = csv.writer(file,delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Directory',                               # 0
                            'Filename',                                 # 1
                            'Date/Time (YYYY:MM:DD HH:MM:SS)',          # 2
                            'GPS Lat',                                  # 3
                            'Lat Ref (N/S)',                            # 4
                            'GPS Long',                                 # 5
                            'Long Ref (W/E)',                           # 6
                            'Current Tags',                             # 7
                            'New Tags (append)',                        # 8
                             'Watermark'])                              # 9
            for asset in file_list:
                # print asset
                metadata.update(et.get_tags(tags, asset))
                # pprint("XMP:Subject = ")
                # pprint(metadata["XMP:Subject"])

                # To make tags more readable
                temp = []
                a = metadata["XMP:Subject"]
                for tag in map(str, a):
                    temp.append(tag)
                temp.sort()
                metadata["XMP:Subject"]=temp

                # pprint(metadata["XMP:Subject"])
                writer.writerow(
                    [metadata["File:Directory"],
                    metadata["File:FileName"],
                    metadata["EXIF:DateTimeOriginal"],
                    metadata["EXIF:GPSLatitude"],
                    metadata["EXIF:GPSLatitudeRef"],
                    metadata["EXIF:GPSLongitude"],
                    metadata["EXIF:GPSLongitudeRef"],
                    metadata["XMP:Subject"]])

        pprint("Generated CSV file: " + csvFile)
        return csvFile

def getCounts(csvFile):
    with open(csvFile) as file:
        reader = csv.reader(file)
        next(reader, None)
        global rowCount
        rowCount = sum(1 for row in reader)
    print("\nTotal images: " + str(rowCount) + "\n")



def copyMeta(fromImage, toImage):
    with exiftool.ExifTool() as et:
        et.execute("-TagsFromFile",
                   fromImage,
                   toImage,
                   "-overwrite_original")

def addWatermark(csvFile):
    print("Watermarking process initiated.")
    folder = raw_input("Drag watermark destination folder here: ").strip() + "/Watermarked_Images/"
    with open(csvFile) as file:
        reader = csv.reader(file)
        next(reader, None)
        with tqdm(total=rowCount) as pbar:
            for row in reader:
                pbar.set_description('Watermarking')
                pbar.update(1)
                fpath = row[0] + "/" + row[1]

                watermark = row[9]
                image = Image.open(fpath, "r")
                draw = ImageDraw.Draw(image)

                fontsize = 2
                #restrict text size to 10% of height of image
                height_fraction = 0.1
                font = ImageFont.truetype("Arial.ttf", fontsize)

                # Fit text onto image
                while (font.getsize(watermark)[1] < height_fraction * image.size[1])\
                        and (font.getsize(watermark)[0] < image.size[0])\
                        and watermark :
                    fontsize += 1
                    font = ImageFont.truetype("Arial.ttf", fontsize)

                # ensure font size isn't too big
                fontsize -= 1
                font = ImageFont.truetype("Arial.ttf", fontsize)
                draw.text((5, 5), watermark, (255, 0, 0, 0), font=font)
                filename = os.path.basename(row[1])
                filename = os.path.splitext(filename)[0]
                wMarkedFilename = filename + '_watermarked.jpg'
                if not os.path.exists(folder):
                    os.makedirs(folder)
                    print("Created Directory: " + folder)
                image.save(folder+wMarkedFilename)
                copyMeta(fpath, folder+wMarkedFilename)
                # print("Saved image to " + folder + wMarkedFilename)
    print("Watermarking process completed.\n")




def wipe(csvFile):
    print("EXIF deletion process initiated.")
    with exiftool.ExifTool() as et:
        with open(csvFile) as file:
            reader = csv.reader(file)
            next(reader, None)
            with tqdm(total=rowCount) as pbar3:
                for row in reader:
                    fpath = row[0] + "/" + row[1]
                    et.execute("-all=",
                               "-overwrite_original",fpath)
    print("EXIF deletion process completed.\n")


def addDateTime(csvFile):
    global rowCount
    print("Date/Time (all) injection process initiated.")
    with exiftool.ExifTool() as et:
        with open(csvFile) as file:
            reader = csv.reader(file)
            next(reader, None)
            with tqdm(total=rowCount) as pbar3:
                for row in reader:
                    pbar3.set_description('Adding GPS')
                    pbar3.update(1)
                    fpath = row[0] + "/" + row[1]
                    datetime = row[2]
                    et.execute("-Time:all=%s" % datetime,
                               "-Make=Nikon",
                               "-Model=D4300",
                               "-overwrite_original",fpath)
    print("Date/Time (all) injection process completed.\n")


def addGPS(csvFile):
    global rowCount
    print("GPS injection process initiated.")
    with exiftool.ExifTool() as et:
        with open(csvFile) as file:
            reader = csv.reader(file)
            next(reader, None)
            with tqdm(total=rowCount) as pbar3:
                for row in reader:
                    pbar3.set_description('Adding GPS')
                    pbar3.update(1)
                    fpath = row[0] + "/" + row[1]

                    if (row[3] and row[4] and row[5] and row[6]):
                        gps_lat = float(row[3])
                        latref = row[4]
                        gps_long = float(row[5])
                        longref = row[6]

                    if (gps_lat and gps_long):
                        et.execute("-GPSLongitudeRef=%s" % longref,
                                   "-GPSLatitudeRef=%s" % latref,
                                   "-GPSLatitude=%f" % gps_lat,
                                   "-GPSLongitude=%f" % gps_long,
                                   "-Make=Nikon",
                                   "-Model=D4300",
                                   "-overwrite_original", fpath)
                    # else: print("Skipped: " + filename)

    print("GPS injection process completed.\n")

def addSubject(csvFile):
    global rowCount
    print("GPS injection process initiated.")
    with exiftool.ExifTool() as et:
        with open(csvFile) as file:
            reader = csv.reader(file)
            next(reader, None)
            with tqdm(total=rowCount) as pbar3:
                for row in reader:
                    pbar3.set_description('Adding GPS')
                    pbar3.update(1)
                    fpath = row[0] + "/" + row[1]
                    final1 = []
                    final2 = []
                    if row[8]:
                        original_tags = row[7][1:-1].split(",")
                        for word in original_tags:
                            word = word.strip()[1:-1].strip()
                            final1.append(word)

                        new_tags = row[8].split(",")
                        for word in new_tags:
                            word = word.strip()
                            final2.append(word)
                        if row[7] != '[]':
                            final2 = list(set(final1).union(set(final2)))
                        final2.sort()
                        for word in final2:
                            et.execute("-Subject+=%s" % word,
                                       "-Make=Nikon",
                                       "-Model=D4300",
                                       "-overwrite_original", fpath)
                    # else: print("Skipped: " + filename)

    print("GPS injection process completed.\n")


def main():
    global rowCount
    global csvFile

    parser = argparse.ArgumentParser(description='Script used to edit EXIF data',
                                    epilog='Example:\npython exif_editor.py\
                                    --wipe true\
                                    --csv true\
                                    --gps true\
                                    --time true\
                                    --watermark true\
                                    --tags true')

    parser.add_argument('--wipe', required=False, help='Wipe EXIF')
    parser.add_argument('--csv', required=False, help='Generate CSV')
    parser.add_argument('--gps', required=False, help='Inject GPS')
    parser.add_argument('--time', required=False, help='Inject Date/Time')
    parser.add_argument('--watermark', required=False, help='Add watermark to image')
    parser.add_argument('--tags', required=False, help='Inject Tags/Keywords')


    args = parser.parse_args()

    if args.csv:
        csvFile = init()
    else:
        csvFile = raw_input("Drag CSV here: ").strip()

    start = time.time()
    getCounts(csvFile)

    if args.wipe:
        wipe(csvFile)
    if args.time:
        addDateTime(csvFile)
    if args.gps:
        addGPS(csvFile)
    if args.tags:
        addSubject(csvFile)
    if args.watermark:
        addWatermark(csvFile)

    end = time.time()
    timePassed = end-start
    print("DONE\n")
    print("Total time: " + str(timePassed))
    print("Avg. time per image: " + str(timePassed/rowCount))
    # init()


if __name__ == "__main__":
    main()