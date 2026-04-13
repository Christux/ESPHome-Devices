import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import display
from esphome.const import CONF_ID

DEPENDENCIES = ["display"]

miniui_ns = cg.esphome_ns.namespace("miniui")

MiniUI = miniui_ns.class_("MiniUI", cg.Component)
Page = miniui_ns.class_("Page")

CONF_DISPLAY_ID = "display_id"
CONF_PAGES = "pages"
CONF_TITLE = "title"
CONF_BODY = "body"
CONF_GUARD = "guard"

PAGE_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(Page),
    cv.Required(CONF_TITLE): cv.string,
    cv.Required(CONF_BODY): cv.lambda_,
    cv.Optional(CONF_GUARD): cv.lambda_,
})

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MiniUI),
    cv.Required(CONF_DISPLAY_ID): cv.use_id(display.Display),
    cv.Required(CONF_PAGES): cv.ensure_list(PAGE_SCHEMA),
}).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    disp = await cg.get_variable(config[CONF_DISPLAY_ID])
    cg.add(var.set_display(disp))

    for conf in config[CONF_PAGES]:
        page = cg.new_Pvariable(conf[CONF_ID])

        cg.add(page.set_title(conf[CONF_TITLE]))

        body = await cg.process_lambda(
            conf[CONF_BODY],
            [(display.DisplayRef, "it")],
            return_type=cg.void
        )
        cg.add(page.set_body(body))

        if CONF_GUARD in conf:
            guard = await cg.process_lambda(
                conf[CONF_GUARD],
                [],
                return_type=cg.bool_
            )
            cg.add(page.set_guard(guard))

        cg.add(var.add_page(page))
