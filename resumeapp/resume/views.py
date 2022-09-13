import os
from flask import Flask, flash, request, redirect, url_for
from resumeapp.resume.forms import ResumeForm
from flask import Blueprint, render_template
from resumeapp.resume.readpdf import readpdffile
from resumeapp.resume.scoring import scoringAndExperienceCheck
from resumeapp.resume.email import sendEmail

resume = Blueprint('resume',__name__)

UPLOAD_FOLDER = 'F:\Python\1. Flask\1. Resume Screening\1. Final'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@resume.route('/index')
def index():
    form = ResumeForm()
    return render_template('index.html', form = form)


@resume.route('/index', methods=['GET','POST'])
def create_post():
    form = ResumeForm()

    if form.validate_on_submit():
        description = form.description.data
        experience = form.experience.data
        primarySkill = form.primarySkill.data
        secondarySkill = form.secondarySkill.data
        emailid = form.emailid.data
        fileName = form.fileName.data
        fileName.save(fileName.filename)
        extractedText = readpdffile(fileName.filename)
        matchPercent, skillsFound, skillsNotFound, experienceInYears, pointsAchieved, pointsLost = scoringAndExperienceCheck(
                                                                            primarySkill, secondarySkill, extractedText)
        experienceInYears = round(experienceInYears, 2)

        #fileName.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
        htmlPage = render_template('output.html',form=form,
                                description = description,
                                experience = experience,
                                primarySkill = primarySkill,
                                secondarySkill = secondarySkill,
                                fileName = fileName.filename,
                                matchPercent = matchPercent,
                                skillsFound = skillsFound,
                                skillsNotFound = skillsNotFound,
                                experienceInYears = experienceInYears,
                                pointsAchieved = pointsAchieved,
                                pointsLost = pointsLost,
                                emailid = emailid
                                )
        sendEmail(emailid, fileName.filename, htmlPage)
        return htmlPage
    return render_template('index.html',form=form)


'''
Skills matched – Points achieved
Skills not matched – Points lost
Experience in years required –
Experience in years available as per resume –
Total Score – Achieved / Total
Score percentage – %
'''
