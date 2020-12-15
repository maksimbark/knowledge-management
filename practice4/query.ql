[out:json];
( area[name="Санкт-Петербург"]; )->.searchArea;

(
  node["tourism"="attraction"](area.searchArea);
  node["tourism"="museum"](area.searchArea);
);


(._;>;);
out body;
