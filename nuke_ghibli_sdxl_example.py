import nuke
import nukescripts
import os
import torch
from PIL import Image
from diffusers import StableDiffusionXLImg2ImgPipeline, ControlNetModel
from controlnet_aux import MidasDetector

#Callback for button
def run_ghibli_stylization():
    node = nuke.thisNode()
    input_node = node.input(0)

    if not input_node or input_node.Class() != "Read":
        nuke.message("Please connect a Read node to this NoOp.")
        return

    input_path = input_node["file"].value()
    if not os.path.exists(input_path):
        nuke.message("Input file not found:\n" + input_path)
        return

    # Get strength value from knob
    strength = node["strength"].value()
    print(f"🎬 Running stylization with strength = {strength}")

    # Load and resize image
    init_image = Image.open(input_path).convert("RGB").resize((900,500))

    # Load ControlNet model for depth
    controlnet = ControlNetModel.from_pretrained(
        "diffusers/controlnet-depth-sdxl-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
        cache_dir=r"D:\hf_diffusion_cache\huggingface\hub"
    )

    # Estimate depth
    depth_estimator = MidasDetector.from_pretrained("lllyasviel/annotators").to("cuda")
    depth_image = depth_estimator(init_image).resize((900,500 ))

    # Load SDXL base pipeline
    pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
        cache_dir=r"D:\hf_diffusion_cache\huggingface\hub"
    ).to("cuda")

    # Load and fuse LoRA
    pipe.load_lora_weights("KappaNeuro/studio-ghibli-style")
    pipe.fuse_lora(lora_scale=0.7)

    # Optimize
    pipe.enable_model_cpu_offload()
    pipe.enable_vae_tiling()

    # Prompt
    prompt = "studio Ghibli-style,dreamy background, anime style, soft shading"
    negative_prompt = "photorealistic, low quality, blurry, CGI, 3D, distorted"

    # Generate image
    generator = torch.Generator("cuda").manual_seed(42)
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=init_image,
        control_image=depth_image,
        strength=strength,
        guidance_scale=17,
        num_inference_steps=50,
        generator=generator
    )

    # Save result
    output_image = result.images[0]
    output_path = os.path.splitext(input_path)[0] + f"_ghibli_strength_{strength:.2f}.png"
    output_image.save(output_path)
    print("✅ Saved:", output_path)

    # Create new Read node and connect
    read_node = nuke.createNode("Read")
    read_node["file"].setValue(output_path)
    read_node.setXYpos(node.xpos() + 150, node.ypos())

#Create the custom NoOp node
def create_ghibli_noop():
    node = nuke.createNode("NoOp")
    node.setName("GhibliStylizer")

    # Run button
    knob = nuke.PyScript_Knob("run_ghibli", "Run Stylization")
    knob.setValue("run_ghibli_stylization()")
    node.addKnob(knob)

    # Strength slider (0 to 1)
    strength_knob = nuke.Double_Knob("strength", "Strength")
    strength_knob.setRange(0.0, 1.0)
    strength_knob.setValue(0.41)  # Default value
    node.addKnob(strength_knob)

    # Register callback
    nukescripts.registerUserFunction("run_ghibli_stylization", run_ghibli_stylization)

create_ghibli_noop()
