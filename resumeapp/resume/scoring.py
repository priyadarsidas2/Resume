import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import time
from googlesearch import search
from newspaper import Article
import random
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('omw-1.4')
stop_words = stopwords.words('english')
stopset = set(nltk.corpus.stopwords.words('english'))
import string
punct = string.punctuation
#lemmatization
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
from datetime import datetime

def scoringAndExperienceCheck(primarySkill, secondarySkill, extractedText):
    df = pd.read_excel("SkillsListv4.xlsx")

    #remove stopwords
    cleaned_text = []
    for word in nltk.word_tokenize(extractedText):
        if word not in punct:
            if word not in stop_words and word.isalpha():
                cleaned_text.append(word)

    cleanedTextAsString = " ".join(cleaned_text)
    skillsFound = []
    for language in df['Skills']:
        if language in cleaned_text:
            skillsFound.append(language)
    skillsFound = list(set(skillsFound))

    skillsNotFound = []
    pointsAchieved = 0

    if primarySkill in cleaned_text:
        pointsAchieved += 50
    else:
        skillsNotFound.append(primarySkill)
    if secondarySkill in cleaned_text:
        pointsAchieved += 25
    else:
        skillsNotFound.append(secondarySkill)

    additionalPoints = 5 * (len(skillsFound) - 2)
    pointsAchieved += additionalPoints
    pointsLost = 100 - pointsAchieved

    matchPercent = pointsAchieved
    matchPercent = round(matchPercent, 2)

    monthsToNum = {"Jan": 1 , "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12, "Sept": 9,
              "January": 1 , "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

    monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    experienceRange = []
    months = []
    years = []

    for i in extractedText.split("\n"):
        for j in monthNames:
            if j in i and "-" in i:
                try:
                    firstPart = i.split(" - ")[0].replace(" ", "").isalpha() == False
                    secondPart = i.split(" - ")[1].replace(" ", "").isalpha() == False
                    if firstPart and secondPart:
                        experienceRange.append(i.split(" - ")[0])
                        experienceRange.append(i.split(" - ")[1])
                    break
                except:
                    pass
            elif j in i and "—" in i and i.split(" — ")[0].isalpha() == False and i.split(" — ")[1].isalpha() == False:
                try:
                    firstPart = i.split(" — ")[0].replace(" ", "").isalpha() == False
                    secondPart = i.split(" — ")[1].replace(" ", "").isalpha() == False
                    if firstPart and secondPart:
                        experienceRange.append(i.split(" — ")[0])
                        experienceRange.append(i.split(" — ")[1])
                    break
                except:
                    pass

    lastExperienceMonthYear = experienceRange[1]
    firstExperienceMonthYear = experienceRange[-2]

    if lastExperienceMonthYear == "Present":
        lastMonth = datetime.now().month
        lastYear = datetime.now().year
    else:
        lastMonth = monthsToNum[lastExperienceMonthYear.split(" ")[0]]
        lastYear = lastExperienceMonthYear.split(" ")[1]
    firstMonth = monthsToNum[firstExperienceMonthYear.split(" ")[0]]
    firstYear = firstExperienceMonthYear.split(" ")[1]
    experienceInYears = (((int(lastYear) - int(firstYear)) * 12) + abs(int(lastMonth) - int(firstMonth)))/12

    return matchPercent, skillsFound, skillsNotFound, experienceInYears, pointsAchieved, pointsLost
