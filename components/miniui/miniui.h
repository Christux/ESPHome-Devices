#pragma once

#include "esphome/core/component.h"
#include "esphome/components/display/display.h"
#include "esphome/core/log.h"
#include <vector>
#include <map>

namespace esphome
{
  namespace miniui
  {
    class MiniUI;

    using BodyFn = std::function<void(display::Display &, MiniUI &)>;
    using GuardFn = std::function<bool(MiniUI &)>;
    using HelperFn = std::function<void(display::Display &, MiniUI &)>;

    class Helper
    {
    public:
      void set_name(const std::string &name);
      void set_function(HelperFn &&func);
      const std::string &get_name() const;
      void call(display::Display &it, MiniUI *ui) const;

    protected:
      std::string name_;
      HelperFn function_;
    };

    class Page
    {
    public:
      void set_title(const std::string &title);
      void set_body(BodyFn &&body);
      void set_guard(GuardFn &&guard);
      bool is_visible(MiniUI *ui) const;
      const std::string &get_title() const;
      void render_content(display::Display &it, MiniUI *ui) const;
      void render(display::Display &it, MiniUI *ui);

    protected:
      std::string title_;
      BodyFn content_;
      GuardFn guard_;
    };

    class MiniUI : public Component
    {
    public:
      void setup() override;
      void loop() override;
      void dump_config() override;
      void set_display(display::Display *display);
      void set_display_writer(display::Display *display);
      void add_page(Page *page);
      void add_helper(Helper *helper);
      void call_helper(const std::string &name, display::Display &it);
      bool has_helper(const std::string &name) const;
      void next_page();
      void prev_page();
      void render(display::Display &it);
      int get_current_index() const;
      Page *get_current_page();
      void update();

    protected:
      display::Display *display_{nullptr};
      std::vector<Page *> pages_;
      std::vector<Helper *> helpers_;
      std::map<std::string, Helper *> helper_map_;
      size_t current_index_{0};
    };

  } // namespace miniui
} // namespace esphome