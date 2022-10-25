# _notepad-pyqt5-python-
i had lots of difficulties putting this together, especially the tab functionality. since it created so many problems in relation to other functionalities, like figuring out how the computer would understand which text editor is currently being used, how to save texts from the current text editor, opening text file's contents onto one of the texteditor's tabs, and many more. I tried experimenting with inheritance and searched all over the internet. only to learn that the solution was getting the index of the currently selected tab and dynamically populating each tab with a separate textbox (that might sound simple, but if you don't know how to program that.. you'll have a very bad time.) fortunately, there are brilliant people in stackoverflow that helped me achieve this. @Alexander @A. Herlas @musicamante these people are legends. (you'll find them wherever the pyqt5 tag exists)
 

the project is still very much in progress, but it made learning pyqt5 an enjoyable process.. even though a confusing one (depending on how ambitious you are).

EDIT:
- lmao!! hahahahaa!!! i just now realized the difference between a rich text editor (eg. microsoft word) vs. a text editor (like notepad). big difference!!
a rich text editor produces a file that can handle fancy colors, tables, bullets, highlighting, etc. while a text editor cannot! simple text editors can only read and create plain text files and nothing else, just purely undecorated texts!! (so that's why when you try to open a .docx file in notepad you get gibberish letters because it can't parse those to .txt format) 

damn.. but luckily i can save the file as .odt, .pdf, or .html extensions which allows a rich form for text editing. all this time i was thinking that i was creating something that can replace the boring notepad, but i was wrong. i didn't even understand clearly the capabilities of both.

anyway, here it is before: [9/5/2022]

![image](https://user-images.githubusercontent.com/43742265/187019107-ba57126e-bc8f-468f-8843-5b730392125a.png)

UPDATE: 

and here it is now: [10/25/2022]

![image](https://user-images.githubusercontent.com/43742265/197763822-02f543bc-a876-47c2-af0a-c757ee64dad3.png)


