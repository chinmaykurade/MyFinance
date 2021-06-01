def get_page_list(page, num_pages):
    if page < 3:
        return list(range(1, page+3))+[None, num_pages]
    elif page > num_pages-3:
        return [1, None]+list(range(page-3, num_pages+1))
    else:
        return [1]+[None]+list(range(page-2, page+3))+[None]+[num_pages]