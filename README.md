# nuke-diffusers-use-examples
Code examples to use huggingface models and LORAs directly in nuke using diffusers.
# Video-Links
https://www.linkedin.com/posts/gunda-pratap_vfx-nuke-compositing-activity-7327130777748414464-7cZO?utm_source=share&utm_medium=member_desktop&rcm=ACoAABOSQCsBCEJyn-YU9zw7k26TQIRfPhs248A

## How It Works?
This runs code directly from scripts editor of nuke without any GUI. We can also create GUI but these are just examples of implementation.
This will import all the required modules to run hugging face models inside nuke. Refer to requrements.txt for required models.
Once we Run the code it will download all the requred model files typically safetensors directly from Huggingface repo.
Once all the requrements are satisfied it will generate the image with give prompts and settings.

## THE PROBLEM!!!!
When we run code we will get errors like 'lzma not found'. This is because nuke python environment doesn't include all the files and modules
Which we get in actual python env we download from python.org.
## SOLLUTION!
Download python installer form python.org. Install it with ADD TO PATH. 
Copy all the files from C:\Users\your_user_name\AppData\Local\Programs\Python\Python310
Paste them in C:\Program Files\Nuke15.1v4. don't override existing files skip them so that it will only paste files not exist.
Now we have have everything required in nuke python env.

## How to Use?
1. Install all modules in requirement.txt into nuke python env.
2. You can use git and run like this - "C:\Program Files\Nuke14.0v5\python.exe" -m pip install module_name
3. Once we install all the modules go to https://huggingface.co/ and create account if not having one.
4. After creating account visit https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
5. Request for access. after authentication we get the access to repo.
6. Open script editor in nuke and direclty copy code from our nuke_ghibli_sdxl_example.py and paste in nuke script editor.
7. Change cache directories in the code to desired locations. example - cache_dir=r"D:\hf_diffusion_cache\huggingface\hub"
8. Hit cntrl+a in script editor and cntrl+enter to run the script.
9. It will create a node called ghibli_stylizer. connect it to read node which You want to conver and hit run button on ghibli_stylizer node.
10. It will start downloading models directly from Huggingface. they are very large in size so it takes time.
11. We can check the process in nuke terminal.
12. Once it gets all the models downloaded, It will generate image and load in a read node.

## Upcoming Features-
GUI to type the prompts and adjust settings like strength, inference_steps.




