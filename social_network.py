import utils
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

def get_practice_graph():
    """Builds and returns the practice graph
    """
    practice_graph = nx.Graph()
    practice_graph.add_edge("A", "C")
    practice_graph.add_edge("A", "B")
    practice_graph.add_edge("B", "C")
    practice_graph.add_edge("B", "D")
    practice_graph.add_edge("D", "C")
    practice_graph.add_edge("D", "E")
    practice_graph.add_edge("D", "F")
    practice_graph.add_edge("C", "F")
    return practice_graph

def draw_practice_graph(graph):
    """Draw practice_graph to the screen.
    """
    nx.draw_networkx(graph)
    plt.show()

def get_romeo_and_juliet_graph():
    """Builds and returns the romeo and juliet graph
    """
    rj = nx.Graph()
    rj.add_edge("Nurse", "Juliet")
    rj.add_edge("Juliet", "Capulet")
    rj.add_edge("Juliet", "Tybalt")
    rj.add_edge("Tybalt", "Capulet")
    rj.add_edge("Juliet", "Romeo")
    rj.add_edge("Juliet", "Friar Laurence")
    rj.add_edge("Romeo", "Friar Laurence")
    rj.add_edge("Romeo", "Benvolio")
    rj.add_edge("Benvolio", "Montague")
    rj.add_edge("Montague", "Romeo")
    rj.add_edge("Romeo", "Mercutio")
    rj.add_edge("Montague", "Escalus")
    rj.add_edge("Escalus", "Mercutio")
    rj.add_edge("Escalus", "Paris")
    rj.add_edge("Paris", "Mercutio")
    rj.add_edge("Paris", "Capulet")
    rj.add_edge("Escalus", "Capulet")
    return rj


def draw_rj(graph):
    """Draw the rj graph to the screen and to a file.
    """
    nx.draw_networkx(graph)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Find and return the friends of friends of the given user.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a set containing the names of all of the friends of
    friends of the user. The set should not contain the user itself
    or their immediate friends.
    """
    friends_set = set()
    friend_func = friends(graph, user)
    for i in friend_func:
        for j in friends(graph, i):
            friends_set.add(j)
    user_set = set()
    user_set.add(user)
    return friends_set - friend_func - user_set


def common_friends(graph, user1, user2):
    """Finds and returns the set of friends that user1 and user2 have in
       common.

    Arguments:
        graph:  the graph object that contains the users
        user1: a string representing one user
        user2: a string representing another user

    Returns: a set containing the friends user1 and user2 have in common
    """
    return friends(graph, user1) & friends(graph, user2)


def number_of_common_friends_map(graph, user):
    """Returns a map (a dictionary), mapping a person to the number of friends
    that person has in common with the given user. The map keys are the
    people who have at least one friend in common with the given user,
    and are neither the given user nor one of the given user's friends.
    Example: a graph called my_graph and user "X"
    Here is what is relevant about my_graph:
        - "X" and "Y" have two friends in common
        - "X" and "Z" have one friend in common
        - "X" and "W" have one friend in common
        - "X" and "V" have no friends in common
        - "X" is friends with "W" (but not with "Y" or "Z")
    Here is what should be returned:
      number_of_common_friends_map(my_graph, "X")  =>   { 'Y':2, 'Z':1 }

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a dictionary mapping each person to the number of (non-zero)
    friends they have in common with the user
    """
    user_common_friend = {}
    variable = friends_of_friends(graph, user)
    for i in variable:
        user_common_friend[i] = len(common_friends(graph, user, i))
    return user_common_friend


def number_map_to_sorted_list(map_with_number_vals):
    """Given a dictionary, return a list of the keys in the dictionary.
    The keys are sorted by the number value they map to, from greatest
    number down to smallest number.
    When two keys map to the same number value, the keys are sorted by their
    natural sort order for whatever type the key is, from least to greatest.

    Arguments:
        map_with_number_vals: a dictionary whose values are numbers

    Returns: a list of keys, sorted by the values in map_with_number_vals
    """
    sorted_list = []
    tuple_from_dict = (map_with_number_vals.items())
    sorted_bychar = sorted(tuple_from_dict, key=itemgetter(0))
    new_sorted = sorted(sorted_bychar, key=itemgetter(1), reverse=True)
    for tuple in new_sorted:
        value = tuple[0]
        sorted_list.append(value)
    return sorted_list


def recommend_by_number_of_common_friends(graph, user):
    """
    Returns a list of friend recommendations for the user, sorted
    by number of friends in common.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: A list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the number of common friends (people
    with the most common friends are listed first).  In the
    case of a tie in number of common friends, the names/IDs are
    sorted by their natural sort order, from least to greatest.
    """
    potential_friends = number_of_common_friends_map(graph, user)
    friends = number_map_to_sorted_list(potential_friends)
    return friends


def influence_map(graph, user):
    """Returns a map (a dictionary) mapping from each person to their
    influence score, with respect to the given user. The map only
    contains people who have at least one friend in common with the given
    user and are neither the user nor one of the users's friends.
    See the assignment writeup for the definition of influence scores.
    """
    friend_iscore = {}
    friends_of_user = friends_of_friends(graph, user)
    for i in friends_of_user:
        sum = 0
        for j in common_friends(graph, user, i):
            sum += 1/(len(friends(graph, j)))
        friend_iscore[i] = sum
    return friend_iscore

def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the influence score (people
    with the biggest influence score are listed first).  In the
    case of a tie in influence score, the names/IDs are sorted
    by their natural sort order, from least to greatest.
    """
    recommendations = influence_map(graph, user)
    return number_map_to_sorted_list(recommendations)

# returns a graoh considting of userID.
def get_facebook_graph():
    """Builds and returns the facebook graph
    """
    facebook = nx.Graph()
    my_file = open("facebook-links.txt")
    for line_of_text in my_file:
        values = line_of_text.split()
        facebook.add_edge(int(values[0]), int(values[1]))
    my_file.close()
    return facebook

def main():
    practice_graph = get_practice_graph()
    draw_practice_graph(practice_graph)

    rj = get_romeo_and_juliet_graph()
    draw_rj(rj)

    # Finds reccomendation differences between common friends and influences
    # scores and prints it a unchanged recommendation and change recmmendation.
    print("Problem 4:")
    print()
    rj_points = rj.nodes()
    unchanged_list = []
    changed_list = []
    for i in rj_points:
        rec_commonfriends = recommend_by_number_of_common_friends(rj, i)
        rec_score = recommend_by_influence(rj, i)
        if rec_commonfriends == rec_score:
            unchanged_list.append(i)
        else:
            changed_list.append(i)
    unchanged_list.sort()
    changed_list.sort()
    print("Unchanged Recommendations:", unchanged_list)
    print("Changed Recommendations:", changed_list)

    # Call and test Facebook graph.
    facebook = get_facebook_graph()

    assert len(facebook.nodes()) == 63731
    assert len(facebook.edges()) == 817090

    print()
    print("Problem 6:")
    print()

    # Finds recommended friends for vailid UserIDs by finding common friends
    # with other users from facebook graph.
    friend_rec = []
    for i in facebook.nodes:
        if i % 1000 == 0:
            friend_rec.append(i)
    friend_rec.sort()
    for j in friend_rec:
        rec_fri_list = recommend_by_number_of_common_friends(facebook, j)
        ten_split_list = rec_fri_list[0:10]
        print(j, "(by num_common_friends):", ten_split_list)

    print()
    print("Problem 7:")
    print()

    # Finds recommended friends for vaild userIDs by finding the influence
    # score based on other friends in the facebook graph.
    for j in friend_rec:
        score_list = recommend_by_influence(facebook, j)
        ten_split_score = score_list[0:10]
        print(j, "(by influence):", ten_split_score)

    print()
    print("Problem 8:")
    print()

    # Finds the number of differences bewteen recommendations from common
    # friends and recommendations fron infleuce scoes.
    common_sum = 0
    different_sum = 0
    for i in friend_rec:
        common = (recommend_by_number_of_common_friends(facebook, i)[1:10])
        iscore = (recommend_by_influence(facebook, i)[1:10])
        if common == iscore:
            common_sum += 1
        else:
            different_sum += 1
    print("Same", common_sum)
    print("Different", different_sum)


if __name__ == "__main__":
    main()
