#pragma once

#include "esphome/core/component.h"
#include "esphome/components/display/display.h"
#include "esphome/core/log.h"
#include <vector>

namespace esphome
{
  namespace miniui
  {
    using BodyFn = std::function<void(display::Display &)>;
    using GuardFn = std::function<bool()>;

    class Page
    {
    public:
      void set_title(const std::string &title);
      void set_body(BodyFn &&body);
      void set_guard(GuardFn &&guard);
      bool is_visible() const;
      const std::string &get_title() const;
      void render_body(display::Display &it) const;
      void render(display::Display &it);

    protected:
      std::string title_;
      BodyFn body_;
      GuardFn guard_;
    };

    class MiniUI : public Component
    {
    public:
      void setup() override;
      void loop() override;
      void dump_config() override;
      void set_display(display::Display *display);
      void add_page(Page *page);
      void next_page();
      void prev_page();
      void render(display::Display &it);
      int get_current_index() const;
      Page *get_current_page();
      void update();

    protected:
      display::Display *display_{nullptr};
      std::vector<Page *> pages_;
      size_t current_index_{0};
    };

  } // namespace miniui
} // namespace esphome