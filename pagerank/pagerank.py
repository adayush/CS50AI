import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    obj = dict()
    for p in corpus.keys():
        obj[p] = (1 - damping_factor)/len(corpus)
        if p in corpus[page]:
            obj[p] += damping_factor/len(corpus[page])

    return obj


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    obj = dict()
    for page in corpus.keys():
        obj[page] = 0
    count = 0

    # choosing first page randomly 
    page = random.choice(list(corpus.keys()))
    obj[page] += 1
    count += 1

    # generating samples
    while True:
        tmodel = transition_model(corpus, page, damping_factor)
        next_page = random.choices(list(tmodel.keys()), weights=tmodel.values(), k=1)[0]
        obj[next_page] += 1
        count += 1
        if count == n:
            break
        page = next_page

    # replacing count with probability in dict
    for key in corpus.keys():
        obj[key] = obj[key]/n
    
    return obj


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    newrank = dict()

    for page in corpus.keys():
        pagerank[page] = 1/len(corpus)
    
    repeat = True
    while repeat:
        for page in pagerank:
            total = float(0)

            for possible_page in corpus:
                # We consider each possible page that links to current page
                if page in corpus[possible_page]:
                    total += pagerank[possible_page] / len(corpus[possible_page])
                # A page that has no links is interpreted as having one link for every page (including itself)
                if not corpus[possible_page]:
                    total += pagerank[possible_page] / len(corpus)

            newrank[page] = (1 - damping_factor) / len(corpus) + damping_factor * total

        repeat = False

        # If any of the values changes by more than the threshold, repeat process
        for page in pagerank:
            if not math.isclose(newrank[page], pagerank[page], abs_tol=0.001):
                repeat = True
            # Assign new values to current values
            pagerank[page] = newrank[page]
    
    return pagerank

if __name__ == "__main__":
    main()
