import nuke
import os
import torch
from PIL import Image
from diffusers import FluxFillPipeline
from diffusers.utils import load_image
from dfloat11 import DFloat11Model


def run_flux_pipeline(image_path, mask_path, output_path, prompt):
    # Optimize memory
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()

    # Load main image and mask
    image = load_image(image_path)
    mask_image = Image.open(mask_path).convert("L")

    # Load FLUX Fill pipeline
    pipe = FluxFillPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-Fill-dev",
        torch_dtype=torch.bfloat16,
        cache_dir=r"D:\hf_cache\huggingface\hub"
    )
    pipe.enable_model_cpu_offload()

    DFloat11Model.from_pretrained(
        'DFloat11/FLUX.1-Fill-dev-DF11',
        device='cpu',
        bfloat16_model=pipe.transformer
    )

    # Run inpainting
    result = pipe(
        prompt=prompt,
        image=image,
        mask_image=mask_image,
        height=512,
        width=512,
        guidance_scale=10,
        num_inference_steps=10,
        max_sequence_length=128,
        generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]

    result.save(output_path)


def flux_process():
    group = nuke.thisNode()
    try:
        main_input = group.input(0)
        mask_writer = group.node("MaskWriter")

        if main_input is None or mask_writer is None:
            raise RuntimeError("Main input or mask writer not connected/found.")

        if main_input.Class() != "Read":
            raise RuntimeError("Main input must be a Read node.")

        # Get image path
        image_path = main_input["file"].value()

        mask_path = mask_writer["file"].value()
        nuke.execute(mask_writer, nuke.root().firstFrame(), nuke.root().firstFrame())

        # Get prompt from group knob
        prompt = group.knob("prompt").value()

        output_path = "C:/Users/pratap/OneDrive/Desktop/inpainting/out_images/flux_output.png"

        # Run the pipeline
        run_flux_pipeline(image_path, mask_path, output_path, prompt)

        # Load output image into Nuke
        output_node = nuke.createNode("Read")
        output_node["file"].setValue(output_path)
        output_node.setXpos(group.xpos() + 100)
        output_node.setYpos(group.ypos() + 100)

    except Exception as e:
        nuke.message(f"FLUX Fill Error: {e}")


def create_flux_group():
    g = nuke.createNode("Group")
    g.setName("FLUX_Fill_Group")
    g.begin()

    # Inputs: 0 = main image, 1 = mask
    input_main = nuke.nodes.Input(name="MainImage")
    input_mask = nuke.nodes.Input(name="MaskInput")

    # Write node to export mask to disk
    write_mask = nuke.nodes.Write(name="MaskWriter")
    write_mask.setInput(0, input_mask)
    write_mask["file"].setValue("C:/Users/pratap/OneDrive/Desktop/dev/mask_temp.png")
    write_mask["file_type"].setValue("png")

    # Output: pass main image through
    output = nuke.nodes.Output()
    output.setInput(0, input_main)
  
    g.end()
  
    # Prompt text input knob
    prompt_knob = nuke.String_Knob("prompt", "Prompt")
    prompt_knob.setValue("")  
    g.addKnob(prompt_knob)

    # Button to run Flux
    run_button = nuke.PyScript_Knob("run_flux", "Run FLUX Fill", "flux_process()")
    g.addKnob(run_button)


# Call this to create the node in the node graph
create_flux_group()
