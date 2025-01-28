import os
from django.core.management.base import BaseCommand
from voter_encoding.models import Cluster

class Command(BaseCommand):
    help = 'Imports cluster data into the database'

    def handle(self, *args, **kwargs):
        # Your cluster_dict with space removed
        cluster_dict = {
            '101': ['193 A', '193 B', '193 C', '193 D', '193 E'],
            '102': ['193 F', '194 A', '194 B', '194 C', '194 D'],
            '103': ['194 E', '195 A', '195 B', '195 C', '195 D', '19 C'],
            '104': ['195 E', '195 F', '195 G', '195 H', '195 I'],
            '105': ['196 A', '196 B', '197 A', '197 B', '198 A', '199 C'],
            '106': ['199 A', '199 B', '200 A', '201 A', '201 B'],
            '107': ['201 C', '202 A', '202 B', '202 C', '202 D', '202 E'],
            '108': ['203 A', '203 B', '204 A', '204 B', '205 A', '206 B'],
            '109': ['206 A', '214 A', '215 A', '215 B', '216 A', '216 C'],
            '110': ['207 A', '208 A', '208 B', '209 A'],
            '111': ['209 B', '210 A', '210 B', '211 A'],
            '112': ['211 B', '212 A', '212 B', '213 A', '213 B'],
            '113': ['216 B', '217 A', '217 B', '217 C', '218 A'],
            '114': ['219 A', '219 B', '219 C', '220 A', '221 A', '221 B'],
            '115': ['222 A', '222 B', '222 C', '222 D', '223 A'],
            '116': ['222 E', '223 B', '223 C', '223 D', '223 E', '224 A', '224 H'],
            '117': ['224 B', '224 C', '224 D', '224 E', '224 F'],
            '118': ['224 G', '225 A', '225 B', '225 C', '225 D'],
            '119': ['225 E', '226 A', '226 B', '227 A', '227 B', '228 A'],
            '120': ['228 B', '228 C', '228 D', '229 A', '229 B', '229 C'],
            '121': ['230 A', '230 B', '231 A', '231 B', '231 C', '232 A'],
            '122': ['232 B', '232 C', '232 D', '232 E', '232 F'],
            '123': ['232 G', '232 H', '232 I', '232 J', '232 K', '232 L']
        }

        # Cleaned cluster_dict: remove spaces from items
        cleaned_cluster_dict = {
            cluster_id: [item.replace(" ", "") for item in items]
            for cluster_id, items in cluster_dict.items()
        }

        # Insert data into the Cluster model
        for cluster_id, items in cleaned_cluster_dict.items():
            Cluster.objects.create(cluster_id=cluster_id, items=items)
        
        self.stdout.write(self.style.SUCCESS('Successfully imported cluster data'))
