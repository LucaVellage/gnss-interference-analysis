import { csvParse, autoType } from "d3-dsv";
import { base } from "$app/paths";

export async function load({ fetch }) {
  const [r1, r2] = await Promise.all([
    fetch(`${base}/data/affected_km2_per_week.csv`),
    fetch(`${base}/data/affected_km2_by_zone_week.csv`),
  ]);
  const [text1, text2] = await Promise.all([r1.text(), r2.text()]);
  return {
    daily: csvParse(text1, autoType),
    byZone: csvParse(text2, autoType),
  };
}