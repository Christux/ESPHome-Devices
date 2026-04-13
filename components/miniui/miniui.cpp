#include "miniui.h"

namespace esphome
{
    namespace miniui
    {
        static const char *const TAG = "miniui";

        void Page::set_title(const std::string &title)
        {
            title_ = std::move(title);
        }

        void Page::set_body(std::function<void(display::Display &)> &&body)
        {
            body_ = std::move(body);
        }

        void Page::set_guard(std::function<bool()> &&guard)
        {
            guard_ = std::move(guard);
        }

        bool Page::is_visible() const
        {
            if (guard_)
                return guard_();
            return true;
        }

        void Page::render(display::Display &it)
        {
            if (body_)
                body_(it);
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

            size_t start = current_index_;
            do
            {
                current_index_ = (current_index_ + 1) % pages_.size();
                if (pages_[current_index_]->is_visible())
                    return;
            } while (current_index_ != start);
        }

        void MiniUI::prev_page()
        {
            if (pages_.empty())
                return;

            size_t start = current_index_;
            do
            {
                current_index_ = (current_index_ + pages_.size() - 1) % pages_.size();
                if (pages_[current_index_]->is_visible())
                    return;
            } while (current_index_ != start);
        }

        void MiniUI::render(display::Display &it)
        {
            if (pages_.empty())
                return;

            size_t start = current_index_;
            while (!pages_[current_index_]->is_visible())
            {
                current_index_ = (current_index_ + 1) % pages_.size();
                if (current_index_ == start)
                    return;
            }

            auto *page = pages_[current_index_];

            ESP_LOGI("miniui", "current page = %d", current_index_);
            ESP_LOGI("miniui", "current page = %s", page->get_title().c_str());

            page->render_body(it);
        }

        int MiniUI::get_current_index() const
        {
            return current_index_;
        }

        Page *MiniUI::get_current_page()
        {
            if (pages_.empty())
                return nullptr;
            return pages_[this->current_index_];
        }
        void MiniUI::update()
        {
            if (!display_)
                return;

            auto *page = get_current_page();
            if (!page)
                return;

            if (!page->is_visible())
                return;

            display_->clear();
            page->render(*display_);
        }

    } // namespace miniui
} // namespace esphome