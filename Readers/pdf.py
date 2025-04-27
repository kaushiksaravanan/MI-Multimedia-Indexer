from pdf2image import convert_from_path
from PIL import Image
import os
from Readers.read_image import *
import shutil
import io


''' falsely identifes some characters  Examlpe 'N' as ']' so I will be removing this
#reference https://stackoverflow.com/a/56055505
def image_to_byte_array(image: Image) -> bytes:
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


TESTING 

D.E. Shaw India Private LimitedAPPLICATION FOR EMPLOYMENTFirst ]ameःLast Name:Date of BirthFather s NameःEmail IDMobile Number:Current Aadress:Permanent Address:When will you be available for internship:Do you have a valid Indian Passport:EDUCATION:DegreeYear ofInstitutionSpecializationGPARank Place inGraduationClassTenthTwelfthBachelorsMastersWORK INTERNSHIP EXPERIENCE:EmployerFromToPositionGross CompensationDE ShawCoD.E. Shaw India Private LimitedSCORES [Competitive Examinationsl:ExaminationYearScore RankJEE MainJEE AdvancedGATEGREState Entrance Exams ( Please Specify )Other Entrance Exams (Please SpecifyCODING CONTEST IParticipation Details]:ContestYearRankACADEMIC SUBJECTS OF INTEREST:Please mention your top 3 Subjects of Interestः1.2.3AWARDS ACHIEVEMENTS HONORS:DeclarationI declare that the information provided in this formis true to the best of my knowledgeIn the event that anyinformation provided is found to be a misrepresentation,would be liable to any action deemedappropriate by the firm.Date:Applicant s signaturePlease attach any additional information which you feel would add to your candidatureDE ShawCo
^
| This is done after converting the pillowobject to bytes array

D.E. Shaw India Private LimitedAPPLICATION FOR EMPLOYMENTFirst NameःLast Name:Date of BirthFather s Name:Email DDMobile Number:Current Address:Permanent Address:When will you be available for internship:Do you have a valid Indian Passport:EDUCATION:DegreeYear ofInstitutionSpecializationGPARank Place inGraduationClassTenthTwelfthBachelorsMastersWORK INTERNSHIP EXPERIENCE:EmployerFromToPositionGross CompensationDE ShawCoD.E. Shaw India Private LimitedSCORES [Competitive Examinations]:ExaminationYearScore RankJEE MainJEE AdvancedGATEGREState Entrance Exams (Please SpecifyOther Entrance Exams (Please Specify )CODING CONTEST IParticipation Details]:ContestYearRankACADEMIC SUBJECTS OF INTEREST:Please mention your3 Subjects of Interest:1.2.3AWARDS ACHIEVEMENTS HONORS:DeclarationI declare that the information provided in this form is true to the best of my knowledgeIn the event that anyinformation provided is found to be a misrepresentation,would be liable to any action deemedappropriate by the firm.Date:Applicant s signaturePlease attach any additional information which you feel would add to your candidatureDE ShawCotop'
^
| This is done by saving files'''

def read_pdf(file_name,poppler_path = r"F:\pyhton lib\Library\bin"):
    temp=file_name
    '''
    parameters are file_name and poopler_path
    poopler_path can be set as an env variable bin folder same with ffmpeg
    '''
    folder='processing'
    os.mkdir(folder)
    path = os.path.join(folder,'image')
    os.mkdir(path)
    shutil.copy(temp, path)
    images = convert_from_path('p.pdf', poppler_path )
    import cv2
    import easyocr
    text=[]
    text2=[]
    reader = easyocr.Reader(['en', 'hi'])
    for i in range(len(images)):
                images[i].save('page'+ str(i) +'.jpg', 'JPEG')
                image = 'page'+str(i)+'.jpg'
                data=read_image(reader,image)
                for i in data:
                    if len(i.split())!=0:
                        text2+=i.split()
                    else:
                        text2+=i
    shutil.rmtree('processing')
    return text2


# print(read_pdf('p2.pdf',r'F:\pyhton lib\Library\bin'))
