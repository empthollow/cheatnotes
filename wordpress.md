# Theme Files

## Pages

- `front-page` # used to display the front page of the site when a static page is set as the front page
- `page.php` # used to display individual pages

## Posts

- `home.php` # used to display the blog posts index page when the front page is set to display the latest posts
- `single.php` # used to display individual blog posts
- `tag.php` # used to display tag archive pages
- `date.php` # used to display date archive pages
- `comments.php` # used to display the comments section on posts and pages
- `paged.php` # used to display paginated archive pages
- `singular.php` # used to display individual posts
- `attachment.php` # used to display attachment pages, such as images, videos; fallback `single.php`

## Agnostic

- `404.php`
- `index.php` # fallback when specific page isn't present
- `style.css`
- `header.php`
- `footer.php`
- `sidebar.php`
- `search.php` # display search results

# Common WordPress Template Tags & Standard Calls (with Examples)

| Function                  | Description                                                  | Example |
|---------------------------|--------------------------------------------------------------|---------|
| **Post Content and Metadata** | | |
| `the_content()`           | Displays the content of a post.                              | `the_content();` |
| `the_excerpt()`           | Displays the post excerpt.                                   | `the_excerpt();` |
| `the_title()`             | Displays the title of the post.                              | `the_title();` |
| `the_permalink()`         | Displays the URL to the post.                                | `echo the_permalink();` |
| `the_ID()`                | Displays the post ID.                                        | `echo the_ID();` |
| `the_author()`            | Displays the post author.                                    | `the_author();` |
| `the_date()`              | Displays the date the post was published.                    | `the_date();` |
| `the_time()`              | Displays the time the post was published.                    | `the_time();` |
| `the_modified_date()`     | Displays the last modified date.                             | `the_modified_date();` |
| **Post Thumbnails (Featured Images)** | | |
| `has_post_thumbnail()`    | Checks if a post has a featured image.                       | `if (has_post_thumbnail()) { ... }` |
| `the_post_thumbnail()`    | Displays the post thumbnail.                                 | `the_post_thumbnail();` |
| **Loop Control** | | |
| `have_posts()`            | Checks if there are posts to show (used in The Loop).        | `if (have_posts()) { while (have_posts()) { the_post(); ... }` |
| `the_post()`              | Sets up post data (used in The Loop).                        | `the_post();` |
| `wp_reset_postdata()`     | Resets post global after custom query.                       | `wp_reset_postdata();` |
| **Navigation** | | |
| `next_post_link()`        | Link to the next post.                                       | `next_post_link();` |
| `previous_post_link()`    | Link to the previous post.                                   | `previous_post_link();` |
| `posts_nav_link()`        | Displays navigation links for posts pages.                   | `posts_nav_link();` |
| `paginate_links()`        | Generates pagination links.                                  | `echo paginate_links();` |
| **Comments** | | |
| `comments_template()`     | Loads the comments template.                                 | `comments_template();` |
| `comment_form()`          | Displays the comment form.                                   | `comment_form();` |
| `wp_list_comments()`      | Displays a list of comments.                                 | `wp_list_comments();` |
| **Categories, Tags, and Taxonomies** | | |
| `the_category()`          | Displays the category of a post.                             | `the_category(', ');` |
| `the_tags()`              | Displays the tags of a post.                                 | `the_tags();` |
| `get_the_terms()`         | Gets terms for a taxonomy (e.g., categories, tags).          | `get_the_terms($post->ID, 'category');` |
| **Menus and Widgets** | | |
| `wp_nav_menu()`           | Displays a custom navigation menu.                           | `wp_nav_menu(['theme_location' => 'primary']);` |
| `dynamic_sidebar()`       | Displays a widget area.                                      | `dynamic_sidebar('sidebar-1');` |
| `register_sidebar()`      | Registers
