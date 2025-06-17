# nuke-diffusers-use-examples
Code examples to use huggingface models and LORAs directly in nuke using diffusers.
# Video-Links
https://www.linkedin.com/posts/gunda-pratap_vfx-nuke-compositing-activity-7327130777748414464-7cZO?utm_source=share&utm_medium=member_desktop&rcm=ACoAABOSQCsBCEJyn-YU9zw7k26TQIRfPhs248A

## How It Works?
this runs code directly from scripts editor of nuke without any GUI. We can also create GUI but these are just examples of implementation.
This will import all the required modules to run hugging face models inside nuke. Refer to requrements.txt for required models.
Once we Run the code it will download all the requred model files typically safetensors directly from Huggingface repo.
once all the requrements are satisfied it will generate the image with give prompts and settings.

## THE PROBLEM!!!!
When we run code we will get errors like 'lzma not found'. This is because nuke python environment doesn't include all the files and modules
which we get in actual python env we download from python.org.
## SOLLUTION!
Download python installer form python.org. Install it with ADD TO PATH. 
copy all the files from C:\Users\your_user_name\AppData\Local\Programs\Python\Python310
paste them in C:\Program Files\Nuke15.1v4. don't override existing files skip them so that it will only paste files not exist.
Now we have have everything required in nuke python env.

## How to Use?
1. Install all modules in requirement.txt into nuke python env.
2. You can use git and run like this - "C:\Program Files\Nuke14.0v5\python.exe" -m pip install module_name
3. once we install all the modules go to https://huggingface.co/ and create account if not having one.
4. after creating account 
5. open script editor in nuke and direclty copy code from our ghibli_sdxl_example.py and paste in nuke script editor.
6. hit cntrl+a in script editor and cntrl+enter to run the script.
7. it will create a node called ghibli hit run button on that node.




