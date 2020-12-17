[out:json];
( area[name="Санкт-Петербург"]; )->.searchArea;

(
  node["tourism"="attraction"](area.searchArea);
  node["tourism"="museum"](area.searchArea);
  node["tourism"="viewpoint"](area.searchArea);
  node["historic"](area.searchArea);
);


(._;>;);
out body;
