# Notebook
Notebook provides easy and geeky way to store fast notes using your command line. 
However when it comes to long notes/articles, Notebook can spawn a WYSIWYG editor for you. 

## Usage
```
nbk I am bored today
nbk --yesterday I bought a new car # Changes file modifcation time
nbk --ui my title # Open a WYSIWYG editor in your browser
```

##Installation
1. Make sure [python](https://www.python.org/downloads/) is installed. (Especially if you are using Windows).   
2. Clone the repo, or [download zip](https://github.com/tabdulradi/notebook/archive/master.zip)
3. Add the following line to your ".bash_profile" file (create it if it doesn't exist)  
```
alias nbk="python /path/to/notebook/src/nbk.py"
```

## TODO
- [ ] GUI for listing all notes
- [ ] GUI for editing notes
- [ ] Better file naming
- [ ] Support for markdown