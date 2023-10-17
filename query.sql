SELECT t1.product_id,
    model,
    t2.name product_name,
    t1.image picture,
    t5.category_id,
    t5.name category_name,
    feed_text description,
    keyword url,
    t1.price rrp,
    t7.price prp
FROM
    oc_product t1
    LEFT JOIN oc_product_description t2 ON t1.product_id = t2.product_id
    LEFT JOIN oc_product_to_category t3 ON t1.product_id = t3.product_id
    LEFT JOIN oc_category t4 ON t3.category_id = t4.category_id
    LEFT JOIN oc_category_description t5 ON t4.category_id = t5.category_id
    LEFT JOIN oc_seo_url t6 ON t1.product_id = SUBSTRING_INDEX(t6.query, '=', -1)
    LEFT JOIN oc_product_special t7 ON t1.product_id = t7.product_id
WHERE query like 'product_id%'
    AND t2.language_id = 1
    AND t5.language_id = 1
    and t6.store_id = 3