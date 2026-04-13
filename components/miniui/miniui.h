#pragma once

#include "esphome/core/component.h"
#include "esphome/components/display/display.h"
#include "esphome/core/log.h"
#include <vector>

namespace esphome
{
  namespace miniui
  {
    class Page
    {
    public:
      void set_title(const std::string &title);
      void set_body(std::function<void(display::Display &)> &&body);
      void set_guard(std::function<bool()> &&guard);
      bool is_visible() const;
      const std::string &get_title() const;
      void render_body(display::Display &it) const;

    protected:
      std::string title_;
      std::function<void(display::Display &)> body_;
      std::function<bool()> guard_;
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

    protected:
      display::Display *display_{nullptr};
      std::vector<Page *> pages_;
      size_t current_{0};
    };

  } // namespace miniui
} // namespace esphome