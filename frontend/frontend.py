import gradio as gr

all_models = ["gpt-3.5-turbo", "alpaca-7b", "claude-v1", "claude-instant-v1", "google/flan-ul2", "google/flan-t5-xxl"]
default_selected_models = [all_models[i] for i in range(2)]
# output_boxes = []
output_rows = []

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
::-webkit-scrollbar {
  width: 4px;
}
::-webkit-scrollbar-track {
  border-radius: 2px;
}
::-webkit-scrollbar-thumb {
  background: #1d4ed8;
  border-radius: 4px;
}
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
    flex-wrap: nowrap;
    padding-right: 16px;
}
#right-column > div {
    overflow: visible;
    flex-wrap: nowrap;
    flex-grow: 1;
}
#right-column > div,
#right-column .text-col,
#right-column .text-col > .form,
#right-column .output-text,
#right-column .output-text > label
 {
    flex-grow: 1;
}
#right-column .output-text > label {
    display: flex;
    flex-direction: column;
    height: 100%;
}
#right-column .output-text > label > textarea {
    flex-grow: 1;
}
#right-column .btn-col {
    min-width: 26px !important;
    flex-grow: 0 !important;   
}
.output-btn {
    padding: 0 !important;
    width: 26px !important;
}
"""
def update_model_selection(selected_models):
    return [gr.Textbox.update(visible = True) if model in selected_models else gr.Textbox.update(visible = False) for model in all_models]

with gr.Blocks(theme=theme, css=css_str, elem_id="container") as demo:
    gr.HTML("<h1>LLM Menagerie</h1>")
    with gr.Row(elem_id="row-0"):
        with gr.Column(elem_id="left-column"):
            text1 = gr.Textbox(label="Prompt", lines=10, elem_id="prompt-input")
            # model_selection_checkboxes = gr.Dropdown(all_models, label="Models", multiselect=True, value=default_selected_models, max_choices=5)
            model_selection_checkboxes = gr.CheckboxGroup(all_models, label="Models", value=default_selected_models)

            run = gr.Button("Run", variant="primary")
            # test = gr.Button(value='\U0001F512', variant="secondary")

        with gr.Column(elem_id="right-column"):
            for model in all_models:
                with gr.Row(visible=(True if model in default_selected_models else False)) as row:
                    output_rows.append(row)
                    with gr.Column(elem_classes=["text-col"]):
                        gr.Textbox(label=model, lines=8, elem_classes=["output-text"])
                    with gr.Column(elem_classes=["btn-col"]):
                        gr.Button(value='\U0001F44D', variant="secondary", elem_classes=["upvote-btn", "output-btn"])
                        gr.Button(value='\U0001F44E', variant="secondary", elem_classes=["downvote-btn", "output-btn"])
                        gr.Button(value='\U00002699', variant="secondary", elem_classes=["setting-btn", "output-btn"])
            model_selection_checkboxes.change(fn=update_model_selection, inputs=model_selection_checkboxes, outputs=output_rows)

demo.launch()