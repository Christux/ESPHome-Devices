import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import display
from esphome.const import CONF_ID

DEPENDENCIES = ["display"]

miniui_ns = cg.esphome_ns.namespace("miniui")

MiniUI = miniui_ns.class_("MiniUI", cg.Component)
Page = miniui_ns.class_("Page")
Helper = miniui_ns.class_("Helper")

CONF_DISPLAY_ID = "display_id"
CONF_PAGES = "pages"
CONF_HELPERS = "helpers"
CONF_NAME = "name"
CONF_TITLE = "title"
CONF_CONTENT = "content"
CONF_GUARD = "guard"

HELPER_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(Helper),
    cv.Required("lambda"): cv.lambda_,
})

PAGE_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(Page),
    cv.Required(CONF_TITLE): cv.string,
    cv.Required(CONF_CONTENT): cv.Schema({
        cv.Required("lambda"): cv.lambda_,
    }),
    cv.Optional(CONF_GUARD): cv.Schema({
        cv.Required("lambda"): cv.lambda_,
    }),
})

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MiniUI),
    cv.Required(CONF_DISPLAY_ID): cv.use_id(display.Display),
    cv.Required(CONF_PAGES): cv.ensure_list(PAGE_SCHEMA),
    cv.Optional(CONF_HELPERS): cv.Schema({
        cv.string: HELPER_SCHEMA,
    }),
}).extend(cv.COMPONENT_SCHEMA)

MiniUIRef = MiniUI.operator("ref")

async def to_code(config):
    miniui = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(miniui, config)

    disp = await cg.get_variable(config[CONF_DISPLAY_ID])
    cg.add(miniui.set_display(disp))

    writer = await cg.process_lambda(
                cv.Lambda(f"id({config[CONF_ID]}).render(it);"),
                [
                    (display.DisplayRef, "it"),
                ],
                return_type=cg.void
            )
    cg.add(disp.set_writer(writer))

    if CONF_HELPERS in config:
        for helper_name, helper_conf in config.get(CONF_HELPERS, {}).items():
            
            helper = cg.new_Pvariable(helper_conf[CONF_ID])
            
            helper_lambda = await cg.process_lambda(
                helper_conf["lambda"],
                [
                    (display.DisplayRef, "it"),
                    (MiniUIRef, "ui"),
                ],
                return_type=cg.void
            )
            
            cg.add(helper.set_name(helper_name))
            cg.add(helper.set_function(helper_lambda))
            cg.add(miniui.add_helper(helper))

    for conf in config[CONF_PAGES]:
        page = cg.new_Pvariable(conf[CONF_ID])

        cg.add(page.set_title(conf[CONF_TITLE]))

        content = await cg.process_lambda(
            conf[CONF_CONTENT]["lambda"],
            [
                (display.DisplayRef, "it"), 
                (MiniUIRef, "ui"),
            ],
            return_type=cg.void
        )
        cg.add(page.set_content(content))

        if CONF_GUARD in conf:
            guard = await cg.process_lambda(
                conf[CONF_GUARD]["lambda"],
                [
                    (MiniUIRef, "ui"),
                ],
                return_type=cg.bool_
            )
            cg.add(page.set_guard(guard))

        cg.add(miniui.add_page(page))
