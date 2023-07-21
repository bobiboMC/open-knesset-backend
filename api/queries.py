def get_member_kns_query(id_field):
         return f"""
                SELECT 
                    f."{id_field}",
                    f."FirstName",
                    f."LastName",
                    f."GenderDesc",
                    f."Email",
                    f."altnames",
                    f."mk_individual_photo",
                    m."faction_name",
                    COALESCE(array_to_string(kns.knesset_array::text[], ', '), '') AS "knesset",
                    COALESCE(json_agg(DISTINCT c."committee_name" || ' (' || c."position_name" || ')') ) AS "committees",
                    CASE WHEN ch."mk_individual_id" IS NOT NULL THEN true ELSE false END AS "IsChairPerson",
                    CONCAT('[', STRING_AGG(DISTINCT CONCAT(year, '-', total_attended_hours), ','), ']') AS year_total_hours_attended
                FROM members_faction_memberships m
                JOIN members_mk_individual f
                    ON f."mk_individual_id" = ANY(ARRAY(SELECT jsonb_array_elements_text(m."member_mk_ids")::integer))
                LEFT JOIN members_mk_individual_committees c
                    ON c."mk_individual_id" = f."mk_individual_id" AND c.finish_date IS NULL
                LEFT JOIN members_mk_individual_faction_chairpersons ch
                    ON ch."mk_individual_id" = f."mk_individual_id"
                LEFT JOIN (
                    SELECT 
                        jsonb_array_elements_text(m.member_mk_ids)::integer AS member_mk_id,
                        array_agg(DISTINCT m.knesset) AS knesset_array
                    FROM members_faction_memberships m
                    GROUP BY member_mk_id
                ) kns ON f."mk_individual_id" = kns.member_mk_id
                LEFT JOIN (
                  SELECT members_presence.mk_id, members_presence.year, SUM(members_presence.total_attended_hours) AS total_attended_hours
                  FROM members_presence
                  GROUP BY members_presence.mk_id, members_presence.year
                ) AS members_presence
                ON f."mk_individual_id" = members_presence.mk_id
                WHERE f."{id_field}"=%s
                GROUP BY f."{id_field}", m."faction_name", f."FirstName", f."LastName", f."GenderDesc", f."IsCurrent", f."Email", f."altnames", f."mk_individual_photo", ch."mk_individual_id", kns."knesset_array"
                ORDER BY m."faction_name" DESC
                LIMIT 1;
    """
	
def get_minister_query(id_field):	
         return f"""
                SELECT
                    f."{id_field}",
                    f."FirstName",
                    f."LastName",
                    f."GenderDesc",
                    f."Email",
                    f."altnames",
                    f."mk_individual_photo",
                    mmif."faction_name",
                    CONCAT('[', STRING_AGG(DISTINCT CONCAT(mmig."govministry_name", ': ', mmig."position_name"), ', '),']') AS ministers,
                    CASE WHEN ch."mk_individual_id" IS NOT NULL THEN true ELSE false END AS "IsChairPerson",
                    COALESCE(array_to_string(kns.knesset_array::text[], ', '), '') AS knessets,
                    COALESCE(json_agg(DISTINCT c."committee_name" || ' (' || c."position_name" || ')') ) AS "committees",
                    CONCAT('[', STRING_AGG(DISTINCT CONCAT(year, '-', total_attended_hours), ', '), ']') AS year_total_hours_attended
                FROM members_mk_individual f
                JOIN members_mk_individual_govministries AS mmig
                    ON mmig."mk_individual_id" = f."mk_individual_id"
                LEFT JOIN members_mk_individual_faction_chairpersons ch
                    ON ch."mk_individual_id" = f."mk_individual_id"
                LEFT JOIN (
                    SELECT
                        jsonb_array_elements_text(m.member_mk_ids)::integer AS member_mk_id,
                        array_agg(DISTINCT m.knesset) AS knesset_array
                    FROM members_faction_memberships m
                    GROUP BY member_mk_id
                ) kns ON f."mk_individual_id" = kns.member_mk_id
                LEFT JOIN (
                  SELECT members_presence.mk_id, members_presence.year, SUM(members_presence.total_attended_hours) AS total_attended_hours
                  FROM members_presence
                  GROUP BY members_presence.mk_id, members_presence.year
                ) AS members_presence
                ON f."mk_individual_id" = members_presence.mk_id
                LEFT JOIN members_mk_individual_factions AS mmif
                ON mmif."mk_individual_id"=f."mk_individual_id" and mmif.knesset=(SELECT max(knesset) FROM members_mk_individual_factions) and mmif."faction_name" NOT LIKE '%%נסגרה%%'
                LEFT JOIN members_mk_individual_committees c
                    ON c."mk_individual_id" = f."mk_individual_id" AND c.finish_date IS NULL
                WHERE mmig.finish_date IS NULL AND f."{id_field}"=%s
                GROUP BY f."{id_field}",
                    f."FirstName",
                    f."LastName",
                    f."GenderDesc",
                    f."IsCurrent",
                    f."Email",
                    f."altnames",
                    f."mk_individual_photo",
                    ch."mk_individual_id",
                    kns."knesset_array",
                    mmif."faction_name";
    """
