# IMDb Scraper

IMDb Scraper is a title scraper for IMDb.

## Current Features
Can scrape titles from search titles from genres.

An example link would be:
```
https://www.imdb.com/search/title/?genres={selected_genre}&sort={selected_sorting}
```

## Run Spider

```commandline
scrapy crawl titles -a genres={YOUR_GENRE} -a sort={YOUR_SORTING}
```

Both genre and sort are optional.

## Future updates
<li>Scrape title page for cast members,</li>
<li>Scrape film ratings data.</li>
