# Images-management
Django rest framework application allowing users to upload images,
## Features
- Users are able to upload images via HTTP request and list their images
- There are three builtin account tiers: `Basic`, `Premium` and `Enterprise`
  - users with `Basic` tier have access to:
      - a link to the thumbnail that's 200px height
  - users with `Premium` tier have access to:
      - a link to the thumbnail that's 200px height
      - a link to the thumbnail that's 400px height
      - a link to original file
  - users with `Enterprise` tier have access to:
      - a link to the thumbnail that's 200px height
      - a link to the thumbnail that's 400px height
      - a link to original file
      - ability to fetch an expiring link to the image (the link expires after a given number of seconds (the user can specify any number between 300 and 30000))

- Admins have ability to create create arbitrary tiers with the following things configurable:
    - arbitrary thumbnail sizes
    - presence of the link to the originally uploaded file
    - ability to generate expiring links
## How to start the project (Windows)
1. Clone this repo `git clone https://github.com/dawdom34/Images-management.git`
2. Now install all required packages `pip install -r requirements.txt`.
3. Create migrations and apply them: `python manage.py makemigrations`, `python manage.py migrate`
4. Run the script to create build in account tiers objects in database: `python manage.py runscript create_default_tiers`
5. Create admin user: `python manage.py createsuperuser`
6. Run the project `python manage.py runserver`
## URLs schema
- User authentication
  - Method: POST
  - URL: `127.0.0.1:8000/login/`
  - Required data:
    - `username`
    - `password`
- Create new account tier
  - Method: POST
  - URL: `127.0.0.1:8000/create_tier/`
  - Rquired data:
    - `name`
    - `thumbnail_size`(Size in pixels as a string with coma separated values eg.'300,400,500')
    - `original_file`(Boolean eg.True/False)
    - `expiring_links`(Boolean)
    - `Token`
- Send image
  - Method: POST
  - URL: `127.0.0.1:8000/image_save/`
  - Required data:
    - `owner`(Id of authenticated user)
    - `image`
    - `Token`
- List all user images
  - Method: GET
  - URL: `127.0.0.1:8000/list_images/`
  - Required data:
    - `Token`
- Get link to original image
  - Method: POST
  - URL: `127.0.0.1:8000/get_original_image/`
  - Required data:
    - `id` (Id of the image)
    - `Token`
- Get thumbnail of image
  - Method: POST
  - URL: `127.0.0.1:8000/get_thumbnail/`
  - Required data:
    - `image_id`
    - `size`
    - `Token`
- Generate expiring link
  - Method: POST
  - URL: `127.0.0.1:8000/generate_expiring_link/`
  - Required data:
    -  `time` (In seconds between 300 and 30000)
    -  `image_id`
    -  `Token`
