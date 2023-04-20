import gradio as gr

all_models = ["gpt-3.5-turbo", "alpaca-7b", "claude-v1", "claude-instant-v1", "google/flan-ul2", "google/flan-t5-xxl"]
default_selected_models = [all_models[i] for i in range(3)]
output_boxes = []

theme = gr.themes.Default(
    primary_hue="blue",
    secondary_hue="blue",
    # spacing_size="spacing_md",
    # radius_size="radius_sm",
).set(
    border_color_accent_dark='*primary_600',
    shadow_spread='20',
    shadow_spread_dark='0',
    button_primary_background_fill='*primary_200',
    button_primary_background_fill_dark='*primary_700',
    button_primary_border_color_dark='*primary_600'
)    

css_str = """
body, gradio-app {
    height: 100vh;
    max-height: 100vh;
}
.main,
.wrap,
.contain,
#component-0 {
    height: 100%;
}
.contain {
    display: flex;
    flex-direction: column;
    overflow: auto;
}
#component-0,
#row-0,
#left-column > .form {
    flex-grow: 1;
    overflow: visible;
}
#row-0 {
    overflow:hidden;
}
#left-column {
    height: 100%;
}
#prompt-input {
    border: 1px solid red;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}
#prompt-input > label {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}
#prompt-input > label > textarea {
    flex-grow: 1;
}
#right-column {
    height: 100%;
    overflow: auto;
    flex-grow: 2 !important;
}
#right-column > .form {
    overflow: visible;
}
"""
def update_model_selection(selected_models):
    return [gr.Textbox.update(visible = True) if model in selected_models else gr.Textbox.update(visible = False) for model in all_models]

with gr.Blocks(theme=theme, css=css_str, elem_id="container") as demo:
    gr.HTML("<h1>LLM Menagerie</h1>")
    with gr.Row(elem_id="row-0"):
        with gr.Column(elem_id="left-column"):
            text1 = gr.Textbox(label="Prompt", lines=10, elem_id="prompt-input")
            model_selection_checkboxes = gr.CheckboxGroup(all_models, label="Models", value=default_selected_models)

            run = gr.Button("Run", variant="primary")

        with gr.Column(elem_id="right-column"):
            output_boxes = [gr.Textbox(label=model, lines=5, visible=(True if model in default_selected_models else False)) for model in all_models]
            model_selection_checkboxes.change(fn=update_model_selection, inputs=model_selection_checkboxes, outputs=output_boxes)

demo.launch()