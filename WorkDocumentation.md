# Keep track of work:

## On 19.03.2024:
- there is an approach of using Pandas and special function in it called **to_latex**. but still I do no know how
  to work with it
- I reached to the first table by pylatex but still I can not control the colors or the size of the columns
- Another idea of working on Latex as a string and modify it using python. its more like using regex to target
  certain parts of the latex text to add the content of the csv file to it. I think this will work well but still I
  do not know a perfect way to do it. Tomorrow we will begin.

## On 20.03.2024:
- I'm going to start bu the idea of yesterday and then see the outcome at the end of the day.
- Something ridiculous happened! I can not make a good table in latex after all uuuuuhhh :\(
- But I think the problem will be solved quickly and chatGPT will help a lot in transformation the Pgfplot library
  into latex very quickly!
- I also did not start in doing anything related to the code part, but do not forget WE HAVE TIME this is not a
  university assignment! :)
- NICE! overleaf has a number of compilations in its free mode!!! and Texmaker, even addon tex in VScode does not
  want to compile the file. UUUUHHHHH.

## On 21.03.2024:
- Starting by solving issues of yesterday, and be ready to give the report.
- Try to stick with a solution or an option.
- The original Project have a problem with text overflow in the tables, especially in the multi-column problems. The
  problem is in my enthronement, as the main project is fine!\
- I will try intelligi environment and see. TEXMAKER is bad!!!
- Intelligi worked perfectly. Now I am trying to find an algorithm to iterate on the latex string in python.
- I tried to use regex, we revisited regex again :(, but I am not good at it, so I think it will take some time till I
  reach a good regex to do !
- There is other option of using bad code, like using for loops over and over again to iterate on a csv file and
  then insert each value in its right place inside the table. This an approach but its a bad and expensive approach.

## On 26.03.2024:
- Finally!! There is a perfect output for the style92, and it works perfectly!!
- Next, I should add more styles and I think I will start with simpler one like style33
- But still, yes we solved the problem or parsing csv files! but still, we need to add al the styles! and this not
  operational in the long run.
- But, we still have time, this is a great start tho!! :)

## On 28.03.2024:
- So I had this idea just at 3 AM this morning while sleeping, I did not even think in the project at all!! But what
  we could say?! HUMAN MIND ><)
- SO, the idea basically came from a bug!! HHAHAHA! When I use pandas to extract out the column names from CSV files,
  in the case of multi-columns, there is empty column names, pandas name it "Unnamed: #".
- FROM THIS, we could actually compute how many multi-columns we have, which makes automating the styles easier and
  very simple. Just by counting the number of "Unnamed" after each column name, we could insert the "\multicolumn{#
  of unnamed+1}{"column name"}" and HUREKAAAA multicolumn problem idea is solved!!
- NOW lets go for the code, which I think will not be finished today, but we will try
- WOOOOOOOOOOOOOOOOOOOOOOOOOOOOW!!!! it worked perfectlllly.....
- I provided logic to ChatGPT for to code, until reaching a FULLY WORKING COMPILER!! on any table on any style.
  الحمد لله.
- Now I have put a TODO for next week, is to make a function that iterates on csv files in a directory and extract
  them into latex files.

## On 02.04.2024
- A lot of complications related to alignments and numbers scientific notations.
- COLUMN margins>>> I need still to specify column margin for each style. This we need me to configure the code according to 9 styles till now!!
- still evey thing is not clear but until next time ISA
- ALso I need to fix problems with INiLLIei

## On 05.04.2024
- Did not do much. I still cannot reach the report style. I compiled the whole project with my style and there a major difference.
- I think the problem will be because the pageplot layout, until next time.

## On 08.04.2024
- Manage to add specific function the determines the first column according to the style number.
- Add it to the main function and it works perfectly.
- The problem is, when I try to insert the output table in the main project, it does not see the new defined column types and also it does not follow the main project style.
- Next time I will see this problem and discuss it with MR. Philip.

# On 17.04.2024
- Solved the problem related to last time. Now the tables work on the main project.
- Added a style file to each table, done automatically.
- there is a problem to the indentation of the first column in the table. I do not how to solve it, but it will ISA.
- Next time I should finish the ToDos.

# On 18.04.2024
- The TODOS are all done the code is now ready to be used on the whole project
- I made a separate file for the new concept to use Alphabet letter as specification for the column types.

# On 24.04.2024
- Used library called "siunitx" in LaTex which allows you to perfectly know how to manipulate the numbers
- the problem is the styling can not be handled well while using.
- I will try to fix the style tomorrow, but the library handles all the special cases perfectly.

# On 25.04.2024
- Managed to solve the problems in the past day and every thing works fine in both my environment and the project environment. Scientific notation DONE
- Next would to determine the styles and column sizes because the column sizes are a very different due to using two libraries together, Taburalx and siunitx. Both of them have their unique environment and handling ways to column sizes.

# On 02.05.2024
- I dived into the core code of the two packages _Siunitx_ and _TabularX_.
- Turned out by skimming the code documentation of _TabularX_ it has some number features like the ones in _Siunitx_, like approximating, aligning numbers around the decimal point...etc
- Next Wednesday, I am going to try those options and see if it fits all the requirements needed for the scientific notations needed in the report.
- I hope it works, as I would save a lot of time coding in pure LaTeX :(. Until next Time....

# On 08.05.2024
- I tried to use the potential of _TabularX_ in cases of alignment around the thousands or decimals separators.
- It worked, but it needs to be added to every number in the table.Also, the alignment around the thousands separator does not work.
- There is a new approach I would like to try, which is to use _Python_ to manipulate the numbers by rounding don the decimals deleting them or according to the case, then add the thousands' separator.
- This is easily will be done next time in python, the problem is, I can not align the numbers around the separator without using _Siunitx_
- I also tried to use macros. The macros need to be added to each number specifically as the new column type generalize the function on all the entries. Which is very bad.

# On 15.05.2024
- Problems. The multicolumn command does not work in _TabularX_ for centring the Title of the multi-columns.
- By putting c in the multicolumn command it works, but then comes the coloring problem!
- SO, I think a solution to such a problem is to make the multicolumn type to always be c and add the color to the text. This will solve the problem.
- Yeah, it solved the problem.
- I won't change anything in the compiler until I tell Mr. Philip.

# 22.05.2024
- Modified the compiler as mentioned last time
- Trying to modify the _siunitx.sty_ with the _tabularx_ width logic.
- Tried a lot of tries with the help of chatgpt put still no hope. But I am optimistic to modify the _siunitx_ column width logic.

# 23.05.2024
- While searching for ways on stackoverflow to mitigate the two libraries together, I found a library called _tabularray_.
- It looks promising, but I need more time to make sure that it can replace _TabularX_.
- I tried some tables with it. It works with the main style of the project, the problem is in the automation of the table and column widths!
- But I think if I dig deeper I could solve such an issue! as it's a parameters problem, at least for now :)
- Until next time....

# 29.05.2024
- Returned back to square 1
- The library does not fit the table in the whole page width!
- Nothing I could do again!

# 05.06.2024
- Developing a UI to make any one use it
- solve the problem of column names if the first column title is empty
- Now I need to deploy it on desktop.
- Maybe for next time..

# 06.06.2024
- Solved the problem of column styles repetition in the second method.
- Learning, again, how to make packages for specific use.
- TODO: deploy the UI. The process will be different in different OS.
- Added the cell color in the multicolumn in the first method and the second when the column type is 'S'.
- Looked at the custom try to find a way to transfer all in code it in to Alphabet.

# 12.06.2024
- Not much done. Spent the day try to recompile the main project but the environment failed.
- The UI is ready to be presented in the next meeting.
- SPENT THE WHOLE DAY FACING THE ELECTRICITY PROBLEM AND INTERNET PROBLEM. I BEGIN TO HATE MY COUNTRY OF ORIGIN!!!!

# 13.06.2024
- Same as the day before without any success :(

# 26.06.2024
- Meeting with the team:
    - presented the solutions.
    - The team chose the second solution _column style base solution_
    - Brainstorming on some of the presented challenges for our colleagues on these solutions.
    - Number of enhancements were presented to add to the solutions chosen >> In ToDos File.

# 27.06.2024
- Begin to organize the tasks mentioned in 26.6.2024 meeting
- Adding a text cell DONE
- Adding a text cell will not process all the files automatically! they will need to choose every file and determine its letter combination.
- There is a miss in the column style and some errors raised.
- I think the problem related to reading the text entered form the text box in the GUI.
- Trying to solve these problems for next time

# 03.07.2024
- Begin to organize the tasks mentioned in 01.07.2024 meeting
- Done some of the Todos up there. The ones related to check boxes.

# 11.07.2024
- Meeting with Philip to discuss the table structures and the letters that will be used.
- We have Format style (Numbers) Layout style (Letters).
- See the ToDo.md for the ToDos.
- Next time I will start to reorganize project by making files for each class and then main file. Make sure the blueprint is okay.

# 24.07.2024
- refactored the code by transforming it to classes
- add the format text cell and the two radio buttons.
- I need to add logic to use them in the main code.

# 25.07.2024
- Added the logic for the Format styling
- Added the trigger tex boxes and censored check box
- Next time, I need to add the logic of the feature above.

# 31.07.2024
- Added the logic for the censorship of certain numbers according to the condition in a certain column.

# 08.08.2024
- Finished the 90 degree column table syntax
- Test it Next time.

# 14.08.2024
- Test for the D column gone successfully
- Added table header and caption features

# 21.08.2024
- Deployed the UI on windows.

# 22.08.2024
- Fixed some bugs.
- Add some user error tests in side the code.
- Fixed the spaces issue after and before the column names.

# 28.08.2024
- Fixed some bugs related to the data after deleting the header/caption columns
- There would be some edits related to the column title names after running latex, it does not wrapp and overflow the cell. We need to add the column name under the \hyphenation{COLUMNNAME with the separators like *Ab-schluss-quote*}. Tried a lot of solutions but this is the only solution.

# 29.08.2024
- Made sure that the app LaTeX output is working with the main project.

# 04.09.2024
- Fixed the importing of styles file into the main project issue

# 05.09.2024
- Make the documentation for the column styles and format style, and added it to the README.md file.

# 11.09.2024
- Meeting with Philipp to discuss the issues and new features.
- Documented all the bugs and the new features to add, begin work tomorrow on it.

# 12.09.2024
- Fixed the CSV encoding problem.
- Deleting the \hline form the last row
- Add thousands grouping, and fixing the decimal point to be in German Format (comma)
- Fixing when the cell is empty for all style numbers to replace with dash (-) except for style number 1 replace with empty space.
- Add note to the UI that if the rows option is chosen in the format style to begin counting from second row.

# 25.09.2024
- Added the trigger value cell with default value is 5.
- Add a note that says its less than the trigger value.
- Write the path selected under the button

# 09.10.2024
- Doing the envelopes task for the QM

# 10.10.2024
- Work on a new version form the app
- Its to take a csv file with names of the tables, and pre-specified for the app variables. The app process this file and set the variables as specified from the file.

# 16.10.2024
- Applied the ideas for compiling the styles CSV.
- Alot of bugs came up. 
- Until next time

# 17.10.2024 
- solved the bugs and the code works perfectly.
- Now I need to add a scrolling to the UI as it's too long.
- Also, I need to add the styles file path selected
- Change the label and format combo box to normal entry!
- Add a function that if there is a new style to give it a name and add to the csv file with its settings.
- Until next time...

# 24.10.2024
- Changed the label and format combo to normal entry
- Add the style file path above the selection button.
- Still need to add scroll to the application Ui because it's too long for the viewer
- Until next time...

# 31.10.2024
- Did not do much
- Tried to enhance the UI desgin

# 07.11.2024
- changed the row csv approach to column. Easier in readability
- Worked on enhancing the UI, maybe adding a scroll bar!
- Still in progress...
- The read styles from file is DONE. waiting for testing by Philip, and then I will merge to main.

# 08.11.2024
- Finished the New UI
- Next time I will make sure that is running smoothly.

# 14.11.2024
- UI tested and everything works perfectly
- Working on collecting all the generated tex files from the converter to a main file to show the files before compiling the whole project.
- till next time

# 15.11.2024
- Finished the main.tex file compilation
- Compiled the project.
