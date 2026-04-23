import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import display, color
from esphome.const import CONF_ID

DEPENDENCIES = ["display"]

miniui_ns = cg.esphome_ns.namespace("miniui")

MiniUI = miniui_ns.class_("MiniUI", cg.Component)
Page = miniui_ns.class_("Page")
Frame = miniui_ns.class_("Frame")
Helper = miniui_ns.class_("Helper")

CONF_DISPLAY_ID = "display_id"
CONF_PAGES = "pages"
CONF_HELPERS = "helpers"
CONF_NAME = "name"
CONF_TITLE = "title"
CONF_ROOT_FRAME = "content"
CONF_X = "x"
CONF_Y = "y"
CONF_WIDTH = "width"
CONF_HEIGHT = "height"
CONF_CHILDREN = "children"
CONF_LAMBDA = "lambda"
CONF_BACKGROUND = "background_color"
CONF_GUARD = "guard"
CONF_DISPLAY_VAR_NAME = "it"
CONF_MINIUI_VAR_NAME = "ui"

HELPER_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(Helper),
    cv.Required(CONF_LAMBDA): cv.lambda_,
})

BASE_FRAME_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(Frame),
    cv.Optional(CONF_X, default=0): cv.int_,
    cv.Optional(CONF_Y, default=0): cv.int_,
    cv.Optional(CONF_WIDTH): cv.int_,
    cv.Optional(CONF_HEIGHT): cv.int_,
    cv.Optional(CONF_LAMBDA): cv.lambda_,
    cv.Optional(CONF_BACKGROUND): cv.use_id(color),
})

FRAME_SCHEMA = BASE_FRAME_SCHEMA.extend({
    cv.Optional(CONF_CHILDREN, default=[]): cv.ensure_list(BASE_FRAME_SCHEMA.extend({
        cv.Optional(CONF_CHILDREN, default=[]): cv.ensure_list(BASE_FRAME_SCHEMA.extend({
            cv.Optional(CONF_CHILDREN, default=[]): cv.ensure_list(BASE_FRAME_SCHEMA.extend({
                cv.Optional(CONF_CHILDREN, default=[]): cv.ensure_list(BASE_FRAME_SCHEMA.extend({
                    cv.Optional(CONF_CHILDREN, default=[]): cv.ensure_list(BASE_FRAME_SCHEMA.extend({
                        cv.Optional(CONF_CHILDREN, default=[]): cv.ensure_list(BASE_FRAME_SCHEMA.extend({
                            cv.Optional(CONF_CHILDREN, default=[]): cv.ensure_list(BASE_FRAME_SCHEMA.extend({
                                cv.Optional(CONF_CHILDREN, default=[]): cv.ensure_list(BASE_FRAME_SCHEMA.extend({
                                    cv.Optional(CONF_CHILDREN, default=[]): cv.ensure_list(BASE_FRAME_SCHEMA),
                                })),
                            })),
                        })),
                    })),
                })),
            })),
        })),
    })),
})

PAGE_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(Page),
    cv.Required(CONF_TITLE): cv.string,
    cv.Required(CONF_ROOT_FRAME): FRAME_SCHEMA,
    cv.Optional(CONF_GUARD): cv.Schema({
        cv.Required(CONF_LAMBDA): cv.lambda_,
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

async def add_set_of_display_writer(config, disp):

    writer = await cg.process_lambda(
        cv.Lambda(f"id({config[CONF_ID]}).render({CONF_DISPLAY_VAR_NAME});"),
        [
            (display.DisplayRef, CONF_DISPLAY_VAR_NAME),
        ],
        return_type=cg.void
    )
    cg.add(disp.set_writer(writer))

async def add_set_of_helpers(config, miniui):

    if CONF_HELPERS in config:

        for helper_name, helper_conf in config.get(CONF_HELPERS, {}).items():
            
            helper = cg.new_Pvariable(helper_conf[CONF_ID])
            
            helper_lambda = await cg.process_lambda(
                helper_conf[CONF_LAMBDA],
                [
                    (display.DisplayRef, CONF_DISPLAY_VAR_NAME),
                    (MiniUIRef, CONF_MINIUI_VAR_NAME),
                ],
                return_type=cg.void
            )
            
            cg.add(helper.set_name(helper_name))
            cg.add(helper.set_function(helper_lambda))
            cg.add(miniui.add_helper(helper))

async def resolve_frame(conf_frame, page, parent_bounds):

    frame = cg.new_Pvariable(conf_frame[CONF_ID])

    bounds = {
        CONF_X: parent_bounds[CONF_X],
        CONF_Y: parent_bounds[CONF_Y],
        CONF_WIDTH: parent_bounds[CONF_WIDTH],
        CONF_HEIGHT: parent_bounds[CONF_HEIGHT]
    }

    for param in bounds.keys():
        if param in conf_frame:
            bounds[param] = bounds[param] + conf_frame[param]

    if CONF_BACKGROUND in conf_frame:

        col = await cg.get_variable(conf_frame[CONF_BACKGROUND])
        cg.add(frame.set_background(col))

    if CONF_LAMBDA in conf_frame:

        content = await cg.process_lambda(
            conf_frame[CONF_LAMBDA],
            [
                (display.DisplayRef, CONF_DISPLAY_VAR_NAME), 
                (MiniUIRef, CONF_MINIUI_VAR_NAME),
            ],
            return_type=cg.void
        )

        cg.add(frame.set_content(content))
        cg.add(frame.set_bounds(bounds[CONF_X], bounds[CONF_Y], bounds[CONF_WIDTH], bounds[CONF_HEIGHT]))
        cg.add(page.add_frame(frame))

    if CONF_CHILDREN in conf_frame:

        for child in conf_frame[CONF_CHILDREN]:

            await resolve_frame(
                conf_frame=child, 
                page=page,
                parent_bounds=bounds
            )

async def add_set_of_pages(config, disp, miniui):

    for conf in config[CONF_PAGES]:
        page = cg.new_Pvariable(conf[CONF_ID])
        cg.add(page.set_title(conf[CONF_TITLE]))

        await resolve_frame(
            conf_frame=conf[CONF_ROOT_FRAME], 
            page=page,
            parent_bounds={
                CONF_X: 0,
                CONF_Y: 0,
                CONF_WIDTH: disp.get_width(),
                CONF_HEIGHT: disp.get_height()
            }
        )

        if CONF_GUARD in conf:

            guard = await cg.process_lambda(
                conf[CONF_GUARD][CONF_LAMBDA],
                [
                    (MiniUIRef, CONF_MINIUI_VAR_NAME),
                ],
                return_type=cg.bool_
            )

            cg.add(page.set_guard(guard))

        cg.add(miniui.add_page(page))

async def to_code(config):

    miniui = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(miniui, config)

    disp = await cg.get_variable(config[CONF_DISPLAY_ID])
    cg.add(miniui.set_display(disp))

    await add_set_of_display_writer(
        config=config,
        disp=disp
    )

    await add_set_of_helpers(
        config=config,
        miniui=miniui
    )

    await add_set_of_pages(
        config=config,
        disp=disp,
        miniui=miniui
    )
