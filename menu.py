from __main__ import igClient

class Home:
    opts = [
        {
            'displayText': 'See & Export your followers list',
            'action': igClient.exportFollowers
        },
        {
            'displayText': 'See & Export your following list',
            'action': igClient.exportFollowing
        },
        {
            'displayText': 'Compare your followers & following lists',
            'action': igClient.compareFollowersAndFollowing
        },
        {
            'displayText': 'Exit',
            'action': exit
        }
    ]

    def display() -> int:
        for i, opt in enumerate(Home.opts):
            print(f'\t{i+1}) {opt["displayText"]}')

        return len(Home.opts)
    

class FolloweeComparison:
    opts = [
        {
            'displayText': 'Export followers that you don\'t follow',
            'value': 'export_followers_you_dont_follow'
        },
        {
            'displayText': 'Export followings that don\'t follow you',
            'value': 'export_followings_that_dont_follow_you'
        },
        {
            'displayText': 'Export all',
            'value': 'export_all'
        }
    ]

    def display() -> int:
            for i, opt in enumerate(FolloweeComparison.opts):
                print(f'\t{i+1}) {opt["displayText"]}')
    
            return len(FolloweeComparison.opts)