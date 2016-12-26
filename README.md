# Multiple Choice Answer Sheet Scanner

## Motivation
Multiple choice answer sheets have long been utilized for machine-grading. However, traditional machine-grading requires various hardware and software, most of which are not free.

Furthermore, traditional bubble sheets are heavily technology-oriented instead of human-oriented, meaning that a lot of design decisions are made just to enable the technology itself, instead of making the user experience easier and smoother. For example, when student fill in the bubble sheets, they need to fill in the bubble for every question. This can be much more time-consuming and non-intuitive than simply writing a letter. Correcting a mistake is also  harder with bubble sheets. On the teacher's end, it extremely tedious to scan all bubble sheets without specialized bubble sheet scanner, reducing the overall marking efficiency. Consequently, the most common practice is that students write their answers in bubble sheets, and the teacher marks them manually.

Therefore, it is desirable to have a multiple choice questions grading system that utilizes tools that are easily accessible to students and teachers, and that is as natural and user-friendly as possible.

## What it does
1. __Prepare:__ This system first generates a specified number of empty answer sheets, each bearing unique information stored in a datamatrix.
2. __Use:__ The teacher distributes the answer sheets to the students in a test. The student may simply write the _letter_ corresponding to the choice in the table. If an answer is wrong, the student may simply cross out the old answer and write a new one next to it.
3. __Grade:__ After collecting the papers, the teacher takes a picture of the papers with a smart phone. It is allowed to include multiple papers in one image as long as the image is clear (an iPhone 7 can handle at least 10 papers at one time with no problem). The program then automatically detects the papers and scan their contents.
4. __Return:__ The program generates a spreadsheet of the results as well as a statistical brief that can be directly exported.