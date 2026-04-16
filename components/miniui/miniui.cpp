#include "miniui.h"

namespace esphome
{
    namespace miniui
    {
        static const char *const TAG = "miniui";

        void Helper::set_name(const std::string &name)
        {
            name_ = name;
        }

        void Helper::set_function(HelperFn &&func)
        {
            function_ = std::move(func);
        }

        const std::string &Helper::get_name() const
        {
            return name_;
        }

        void Helper::call(display::Display &it, MiniUI *ui) const
        {
            if (function_)
                function_(it, *ui);
        }

        // Implémentation de Page
        void Page::set_title(const std::string &title)
        {
            title_ = title;
        }

        void Page::set_body(BodyFn &&body)
        {
            body_ = std::move(body);
        }

        void Page::set_guard(GuardFn &&guard)
        {
            guard_ = std::move(guard);
        }

        bool Page::is_visible(MiniUI *ui) const
        {
            if (guard_)
                return guard_(*ui);
            return true;
        }

        void Page::render(display::Display &it, MiniUI *ui)
        {
            if (body_)
                body_(it, *ui);
        }

        const std::string &Page::get_title() const
        {
            return title_;
        }

        void Page::render_body(display::Display &it, MiniUI *ui) const
        {
            if (body_)
            {
                body_(it, *ui);
            }
            else
            {
                ESP_LOGE(TAG, "No lambda set for page body %s", get_title().c_str());
            }
        }

        // Implémentation de MiniUI
        void MiniUI::setup()
        {
        }

        void MiniUI::loop()
        {
        }

        void MiniUI::dump_config()
        {
            ESP_LOGCONFIG(TAG, "MiniUI with %d pages and %d helpers", pages_.size(), helpers_.size());
            for (auto *helper : helpers_)
            {
                ESP_LOGCONFIG(TAG, "  Helper: %s", helper->get_name().c_str());
            }
        }

        void MiniUI::set_display(display::Display *display)
        {
            display_ = display;
            set_display_writer(display_);
        }

        void MiniUI::set_display_writer(display::Display *display)
        {
            display_->set_writer(
                [&](display::Display &it)
                { 
                    this->render(it); 
                }
            );
        }

        void MiniUI::add_page(Page *page)
        {
            pages_.push_back(page);
        }

        void MiniUI::add_helper(Helper *helper)
        {
            helpers_.push_back(helper);
            helper_map_[helper->get_name()] = helper;
        }

        void MiniUI::call_helper(const std::string &name, display::Display &it)
        {
            auto it_helper = helper_map_.find(name);
            if (it_helper != helper_map_.end())
            {
                it_helper->second->call(it, this);
            }
            else
            {
                ESP_LOGW(TAG, "Helper '%s' not found", name.c_str());
            }
        }

        bool MiniUI::has_helper(const std::string &name) const
        {
            return helper_map_.find(name) != helper_map_.end();
        }

        void MiniUI::next_page()
        {
            if (pages_.empty())
                return;

            size_t start = current_index_;
            do
            {
                current_index_ = (current_index_ + 1) % pages_.size();
                if (pages_[current_index_]->is_visible(this))
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
                if (pages_[current_index_]->is_visible(this))
                    return;
            } while (current_index_ != start);
        }

        void MiniUI::render(display::Display &it)
        {
            if (pages_.empty())
                return;

            size_t start = current_index_;
            while (!pages_[current_index_]->is_visible(this))
            {
                current_index_ = (current_index_ + 1) % pages_.size();
                if (current_index_ == start)
                    return;
            }

            auto *page = pages_[current_index_];

            ESP_LOGI("miniui", "current page = %d", current_index_);
            ESP_LOGI("miniui", "current page = %s", page->get_title().c_str());

            page->render_body(it, this);
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
            display_->clear();
            display_->update();
        }

    } // namespace miniui
} // namespace esphome