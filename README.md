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
- Intelligi worked perfectlly. Now I am trying to find an algorithm to iterate on the latex string in python.
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