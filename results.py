import os
import csv
import constants
from shutil import copyfile
from collections import defaultdict

#

class Result:
    colours = ["red", "pink", "purple", "deep-purple ", "indigo", "blue", "light_blue",
               "cyan", "teal", "green", "light-green", "lime", "yellow", "amber", "orange",
               "deep-orange", "brown", "grey", "blue-grey"]

    def __init__(self, files, message, addr, sorted_score, sorted_distro, method, file_map=None, tile_map = None):
        self.results_dir = addr + "/results"  # Stores where the results will be stored
        if not os.path.exists(self.results_dir):
            os.mkdir(self.results_dir)

        self.files = files
        self.message = message
        self.sorted_score = sorted_score
        self.sorted_distro = sorted_distro
        self.method = method
        self.file_map = file_map
        self.tile_map = tile_map

        self.template = None
        self.match_map = {}
        self.hash_map = defaultdict(list)
        self.create_hash_map()

    def get_hm(self):
        return self.hash_map

    def create_hash_map(self):
        for x in self.sorted_score:
            score = x[1]
            if score > constants.SIMILARITY_THRESHOLD:
                file_1 = x[0][0]
                file_2 = x[0][1]
                # print(str(file_1) + " " + str(file_2))
                self.hash_map[file_1].append((file_2, score))
                self.hash_map[file_2].append((file_1, score))

    def print_csv(self):
        results_file_addr = self.results_dir + "/" + self.method + "_results.csv"

        with open(results_file_addr, mode='w', newline='') as results_file:
            results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for val in self.sorted_scores:
                files = list(val[0])  # gets both filenames and puts them into a list
                score = val[1]
                if score > constants.SIMILARITY_THRESHOLD:
                    files.append(score)
                    results_writer.writerow(files)
                    # f.write("Similarity Score for " + str(key) + " is : " + str(score))

    def print_match(self):
        self.template = open("materialize/match_template.html")
        out_template = "".join(self.template.readlines())
        match_dir = self.results_dir + "/matches_" + self.method
        if not os.path.exists(match_dir):
            os.mkdir(match_dir)
        print(self.sorted_score)
        for index, data in enumerate(self.sorted_score):
            output_file = out_template
            filename = "match-" + str(index) + ".html"
            filename_1 = data[0][0]
            filename_2 = data[0][1]
            if filename_1[0] == "\\":
                filename_1 = filename_1[1:]
            if filename_2[0] == "\\":
                filename_2 = filename_2[1:]
            score = data[1]
            score = int(score * 100) / 100

            if score < constants.SIMILARITY_THRESHOLD:
                continue

            # print(str(filename_1) + str(filename_2))
            hash1 = hash(filename_1)
            hash2 = hash(filename_2)
            if hash1 >= hash2:
                key = (filename_1, filename_2)
            else:
                key = (filename_2, filename_1)

            self.match_map[key] = index

            output_file = output_file.replace("<!--filename1-->", filename_1)
            output_file = output_file.replace("<!--filename2-->", filename_2)
            output_file = output_file.replace("<!--score-->", str(score))
            output_file = output_file.replace("<!--method-->", self.method)
            output_f = match_dir + "/" + filename

            f = open(output_f, 'w')


            file1 = self.file_map[filename_1]
            file2 = self.file_map[filename_2]

            code_str = "<code>  <!--line--></code>"
            copied_code_str = "<code class='<!--colour--> lighten-3'>  <!--line--></code>"
            file_1_str = ""
            file_2_str = ""

            # Loops through tile map and gets all the line numbers where the tokens were the same
            copied_lines_1 = []
            copied_lines_2 = []
            colour_picker = 0

            # Used to show table of match line numbers at the end of each file
            match_table = """
                            <tr class="<!--colour--> lighten-3">
                                <td><!--file1--> (<!--start1-->, <!--end1-->)</td>
                                <td><!--file2--> (<!--start2-->, <!--end2-->)</td>
                                <td><!--numtokens--></td>
                            </tr>"""
            match_table_str = ""

            match_str = match_table.replace("<!--file1-->", key[0])
            match_str = match_str.replace("<!--file2-->", key[1])

            # Looping through each tile match-------------------------
            # Dictionary used to store the colours of lines with matches
            line_colour_map_1 = {}
            line_colour_map_2 = {}
            if self.method != "ml":
                for tiles in self.tile_map[key]:
                    colour_picker += 1
                    colour_picker = colour_picker % len(Result.colours)
                    temp_match_str = match_str.replace("<!--colour-->", Result.colours[colour_picker])

                    start = tiles[1][0]
                    end = tiles[1][1]
                    numtokens = end - start + 1

                    temp_match_str = temp_match_str.replace("<!--start1-->", str(start))
                    temp_match_str = temp_match_str.replace("<!--end1-->", str(end))
                    temp_match_str = temp_match_str.replace("<!--numtokens-->", str(numtokens))

                    temp = [i for i in range(start, end+1)]
                    for i in temp:
                        line_colour_map_1[i] = Result.colours[colour_picker]

                    start = tiles[2][0]
                    end = tiles[2][1]

                    temp_match_str = temp_match_str.replace("<!--start2-->", str(start))
                    temp_match_str = temp_match_str.replace("<!--end2-->", str(end))
                    temp = [i for i in range(start, end + 1)]
                    for i in temp:
                        line_colour_map_2[i] = Result.colours[colour_picker]

                    match_table_str += temp_match_str

            line_count = 1
            for line in file1.split("\n"):
                if line_count in line_colour_map_1:
                    new_code = copied_code_str.replace("<!--line-->", line)
                    new_code = new_code.replace("<!--colour-->", line_colour_map_1[line_count])
                else:
                    new_code = code_str.replace("<!--line-->", line)
                file_1_str += new_code
                line_count += 1

            line_count = 1
            for line in file2.split("\n"):
                if line_count in line_colour_map_2:
                    new_code = copied_code_str.replace("<!--line-->", line)
                    new_code = new_code.replace("<!--colour-->", line_colour_map_2[line_count])
                else:
                    new_code = code_str.replace("<!--line-->", line)
                file_2_str += new_code
                line_count += 1

            output_file = output_file.replace("<!--bottomtable-->", match_table_str)
            output_file = output_file.replace("<!--file1code-->", file_1_str)
            output_file = output_file.replace("<!--file2code-->", file_2_str)
            f.write(output_file)
            f.close()

    def print_html(self):

        self.print_match()  # print list of matches

        self.template = open("materialize/template.html")

        results_file_addr = self.results_dir + "/" + self.method + "_results.html"
        javascript_dir = self.results_dir + "/js"
        css_dir = self.results_dir + "/css"
        match_dir = self.results_dir + "/matches_" + self.method

        if not os.path.exists(javascript_dir):
            os.mkdir(javascript_dir)
        if not os.path.exists(css_dir):
            os.mkdir(css_dir)

        copyfile("materialize/materialize.min.css", css_dir + "/materialize.min.css")
        copyfile("materialize/materialize.min.js", javascript_dir + "/materialize.min.js")

        f = open(results_file_addr, 'w')
        output_file = "".join(self.template.readlines())

        file_list = ""
        for x in self.files:
            file_list += str(x) + " - "
        file_list = file_list[:-2]

        num_files = len(self.files)  # gets the length of files scanned
        num_matches = len(self.sorted_score)

        distro_table = ""
        template_str = """
        <tr>
            <td><b><!--bucket--></b></td>
            <td><!--num--></td>
        </tr>"""
        for x in self.sorted_distro:
            b = str(x[0] - 10) + "% - " + str(x[0]) + "%"
            temp = template_str.replace("<!--bucket-->", str(x[0]))
            temp = temp.replace("<!--num-->", str(x[1]))
            distro_table += temp

        template_str = """
                <tr>
                    <td><b><!--filename--></b></td>
                    <td>&rarr;</td>
                    <!--comparisons-->
                </tr>"""
        comparison_str = """
        <td><a href="matches_<!--method-->/match-<!--matchno-->.html"><!--filename--></a><br><!--score-->%</td>"""

        avg_similarity_str = ""
        for k, v in self.hash_map.items():
            filename = k
            temp = template_str.replace("<!--filename-->", filename)
            all_comparisons = ""
            for comparison in v:
                fname = comparison[0]

                if len(self.match_map)!= 0:
                    if (filename, fname) in self.match_map:
                        matchno = self.match_map[(filename, fname)]
                    elif (fname, filename) in self.match_map:
                        matchno = self.match_map[(fname, filename)]
                else:
                    matchno = 0

                score = int(comparison[1] * 100) / 100
                c = comparison_str.replace("<!--filename-->", fname)
                c = c.replace("<!--score-->", str(score))
                c = c.replace("<!--method-->", self.method)

                c = c.replace("<!--matchno-->", str(matchno))
                all_comparisons += c
            temp = temp.replace("<!--comparisons-->", all_comparisons)
            avg_similarity_str += temp

        output_file = output_file.replace("<!--comparison description-->", self.message)
        output_file = output_file.replace("<!--file list-->", file_list)
        output_file = output_file.replace("<!--num files-->", str(num_files))
        output_file = output_file.replace("<!--num matches-->", str(num_matches))
        output_file = output_file.replace("<!--min threshold-->", str(constants.SIMILARITY_THRESHOLD))
        output_file = output_file.replace("<!--distrobution table-->", distro_table)
        output_file = output_file.replace("<!--avgsim-->", avg_similarity_str)

        if self.method =="quick_gst":
            output_file = output_file.replace("<!--method-->", "Improved Greedy String Tiling")
        elif self.method == "ml":
            output_file = output_file.replace("<!--method-->", "Attribute Counting using Machine Learning")


        f.write(output_file)
        f.close()
