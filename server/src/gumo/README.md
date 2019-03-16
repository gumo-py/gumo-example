# gumo

Google User's MOdule for GAE/Python3.7


## Usage

```bash
$ pip install gumo-datastore gumo-tasks
```

## Configuration

```py
import os
import gumo
from gumo.infra import datastore
from gumo.infra.datastore import converter as datastore_converter
from gumo.infra import tasks
from gumo.infra.tasks import emulator as tasks_emulator

# 全てデフォルト値の場合には、引数無指定で呼び出せばOK
# gumo.configure_once()

# gumo.initialize() の中で実行すれば、ライブラリ間の依存関係チェックをその終了時まで遅延する
with gumo.initialize():
    gumo.configure_once(
        google_cloud_project=os.environ.get('GOOGLE_CLOUD_PROJECT'),
        google_cloud_location=os.environ.get('GOOGLE_CLOUD_LOCATION'),
    )

    datastore.configure_once(
        use_local_emulator=os.environ.get('DATASTORE_LOCAL_EMULATOR_ENABLED'),
        emulator_host=os.environ.get('DATASTORE_EMULATOR_HOST'),
        namespece=os.environ.get('DATASTORE_NAMESPACE'),
    )

    # datastore_converter を利用するには datastore と tasks の両方が必要
    # 上から順に評価するとこの時点では tasks が初期化前なのでエラーになる
    datastore_converter.configure_once(
        tasks_queue_name='convert',
    )

    tasks.configure_once(
        persist_datastore=os.environ.get('TASKS_PERSIST_DATASTORE_ENABLED'),
        persist_datastore_kind=os.environ.get('TASKS_PERSIST_DATASTORE_KIND')
    )

    tasks_emulator.configure_once(
        persist_datastore_kind=os.environ.get('TASKS_PERSIST_DATASTORE_KIND'),
    )
```

## Package Structures

```py
# fundamental という言葉(語感)が気に入ったので入れてみたレベル
from gumo.fundamental import EntityKey

# datastore とかは
from gumo.infra import datastore

class DatastoreHelloRepository(HelloRepository, datastore.RepositoryMixin):
    # datastore.RepositoryMixin が幾つかのメソッドを提供する
    # (mixinで継承・混ぜ込むの良くないので、移譲する形にしたい....)
    #
    # self._to_raw_key : EntityKey から datastore Key を得る
    # self._build_raw_entity : datastore Entity を作る
    # self.client : datastore.Client そのもの
    #
    # gumo.infra.datastore の中には、
    #   1. gumo の世界と、
    #   2. google.cloud.datastore の世界と、
    #   3. 両者を変換するツール、
    # の3種が混在する。これらを良い感じに区別しながら扱いやすい形に整理したい。
    #
    def create(self, entity: HelloEntity):
        key = self._to_raw_key(entity.key) # -> google.cloud.datastore.Key
        o = self._build_raw_entity(key) # -> google.cloud.datastore.Entity
        o.update(
            HelloEntityMapper.serialize(entity)  # -> dict
        )

        self.client.put(o)
```
