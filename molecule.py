import re
def parse_molecule (formula):
  #for the formula input, lets pick out all of the elements and put them in a set:
    elems="".join([i for i in formula if i.isalpha()])
    mols = set(re.findall('[A-Z][^A-Z]*', elems))

  #okay now lets find the position of each element (including repeats)
  #in the chemical equation.  This will return a list of lists, each element in order,
  #with its position in the equation:
    elempositions=[]
    for m in mols:
        for x in re.finditer(m, formula):
            elempositions.append([x.group(0),x.start()])

  #now some quick cleanup.  first lets remove instances where our above regex
  #failed (oops) and counted 2-letter elements (like 'Cu') twice (as both 'C' and 'Cu').
  #now each position of the capital letter of the element is stored, with no duplicates
    for x in elempositions:
        pos=x[1]
        for y in elempositions:
            if y[1]==x[1] and x[0]!=y[0] and len(y[0]) ==1:
                elempositions.remove(y)

  #more cleanup - if it is a 2-letter element, lets set the position at the 2nd (lowercase)
  #letter.  This will become relevant later when we start examining characters AFTER
  #the element.
    for elem in elempositions:
        if len(elem[0])==2:
            elem[1]+=1
  #perfect, now we have our list of the last letter of an element
  #and its corresponding position in the formula

  #okay, down to business.  for each element, lets look at the numbers and brackets
  #AFTER that element, and do some math based on what we find!

  #this list will hold the final count (# atoms) for each element in the formula
    elemsfinal=[]
    for elem in elempositions:
        formulalist=list(formula)
  #this helper function will be used to check if there is a number (subscript)
  #immediately following the element
        def RepresentsInt(s):
            try:
                int(s)
                return True
            except ValueError:
                return False
  #for each instance of an element, grab the number directly to the right.
  #or just set=1 if no number.  This is our initial number of atoms
        if elem[1]==len(formula)-1:
            elem1count=1
        else:
            nextchar=formulalist[elem[1]+1]
            if RepresentsInt(nextchar):
                elem1count=int(re.search(r"(^[A-z]\d+)",formula[elem[1]:]).group()[1:])
            else:
                elem1count=1
  #okay we got the initial subscript for the element.  now lets move forward to the end of the formula.
  #numbers always come after brackets, BUT here's the kicker: that number only applies
  #IF the closing bracket included that element.  How do we make sure that the element
  #was inside a particular closing bracket??  Answer: if MORE BRACKETS HAVE CLOSED THAN
  #HAVE OPENED AFTER THAT ELEMENT.  Like counting cards, we'll keep a count of the closing brackets.
  #when the count hits -1, we know that the next number WILL be a multiplier for this element.
            bracketcount=0
            for char in formulalist[elem[1]:len(formulalist)+1]:
                if bracketcount<0 and RepresentsInt(char):
                    elem1count=elem1count*int(char)
                    bracketcount=0
                elif bracketcount<0:
                    elem1count=elem1count
                    bracketcount=0
                if char in ['[','{','(']:
                    bracketcount+=1
                elif char in [']','}',')']:
                    bracketcount-=1
        elemtoadd=[elem[0],elem1count]
        elemsfinal.append(elemtoadd)

  #perfect, now 'elemsfinal' holds each element plus its atom count.
  #however, there are duplicates, so we need to combine totals where the element
  #is the same.  Put those in a dictionary, and we are done with counting atoms!
    elemsdict={}
    for x in elemsfinal:
        if x[0] in elemsdict:
            elemsdict[x[0]]+=x[1]
        else:
            elemsdict[x[0]]=x[1]
    print(elemsdict)
    return elemsdict

parse_molecule("As2{Be4C5[BCo3(CO2)3]2}4Cu5")
