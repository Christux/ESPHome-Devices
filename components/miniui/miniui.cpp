#include "miniui.h"

namespace esphome
{
    namespace miniui
    {
        static const char *const TAG = "miniui";

        void Page::set_title(const std::string &title)
        {
            title_ = title;
        }

        void Page::set_body(std::function<void(display::Display &)> &&body)
        {
            body_ = body;
        }

        void Page::set_guard(std::function<bool()> &&guard)
        {
            guard_ = guard;
        }

        bool Page::is_visible() const
        {
            if (guard_)
                return guard_();
            return true;
        }

        const std::string &Page::get_title() const
        {
            return title_;
        }

        void Page::render_body(display::Display &it) const
        {
            if (body_)
            {
                body_(it);
            }
            else
            {
                ESP_LOGE(TAG, "No lambda set for page body %s", get_title().c_str());
            }
        }

        void MiniUI::setup()
        {
        }

        void MiniUI::loop()
        {
        }

        void MiniUI::dump_config()
        {
            ESP_LOGCONFIG(TAG, "Empty component");
        }

        void MiniUI::set_display(display::Display *display)
        {
            display_ = display;
        }

        void MiniUI::add_page(Page *page)
        {
            pages_.push_back(page);
        }

        void MiniUI::next_page()
        {
            if (pages_.empty())
                return;

            size_t start = current_;
            do
            {
                current_ = (current_ + 1) % pages_.size();
                if (pages_[current_]->is_visible())
                    return;
            } while (current_ != start);
        }

        void MiniUI::prev_page()
        {
            if (pages_.empty())
                return;

            size_t start = current_;
            do
            {
                current_ = (current_ + pages_.size() - 1) % pages_.size();
                if (pages_[current_]->is_visible())
                    return;
            } while (current_ != start);
        }

        void MiniUI::render(display::Display &it)
        {
            if (pages_.empty())
                return;

            size_t start = current_;
            while (!pages_[current_]->is_visible())
            {
                current_ = (current_ + 1) % pages_.size();
                if (current_ == start)
                    return;
            }

            auto *page = pages_[current_];

            ESP_LOGI("miniui", "current page = %d", current_);
            ESP_LOGI("miniui", "current page = %s", page->get_title().c_str());

            page->render_body(it);
        }

    } // namespace miniui
} // namespace esphome