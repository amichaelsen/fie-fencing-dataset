def save_dict_to_cache(cache_filename, dict_key, dict_value):

    # save data to cache for potential future use (even if not drawing from cache)
    if((not path.exists(cache_filename)) or (stat(cache_filename).st_size == 0)):
        # cache file does not exist or is empty (cannt be json.loaded)
        with open(cache_filename, 'w') as write_file:
            new_cache_dict = {dict_key: dict_value}
            json.dump(new_cache_dict, write_file)
    else:
        with open(cache_filename) as read_file:
            cached_data = json.load(read_file)
            # store tournament dict, overwrite old data if it exists
            cached_data[dict_key] = dict_value
            with open(cache_filename, 'w') as write_file:
                json.dump(cached_data, write_file)
