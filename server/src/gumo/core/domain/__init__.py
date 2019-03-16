import dataclasses


@dataclasses.dataclass(frozen=True)
class GoogleCloudProjectID:
    project_id: str

    def __post_init__(self):
        if not isinstance(self.project_id, str):
            raise ValueError(f'project_id must be a string, expect: {type(self.project_id)}')


@dataclasses.dataclass(frozen=True)
class GoogleCloudLocation:
    # TODO: リージョン一覧の取得は、 Google Compute Engine の API を利用して取得できるようにしたい
    #
    # Python 用の Google API Client Library を利用し、Compute Engine API の リージョン一覧
    # メソッドを使用することより、現在利用可能なリージョン一覧を取得できます。
    #
    # Google API Client Library for Python については、
    # 以下のリンク： [1] をご参照ください。
    #
    # また、Compute Engine API のリージョン一覧メソッドにつきましては、
    # 以下のリンク ：[2] をご参照ください。
    #
    # [1] https://developers.google.com/api-client-library/python/apis/compute/v1
    # [2] https://developers.google.com/resources/api-libraries/documentation/compute/v1/python/latest/compute_v1.regions.html#list
    AVAILABLE_LOCATIONS = [
        'us-west1',  # オレゴン
        'us-west2',  # ロサンゼルス
        'us-central1',  # アイオワ
        'us-east1',  # サウスカロライナ
        'us-east4',  # 北バージニア
        'northamerica-northeast1',  # モントリオール
        'southamerica-east1',  # サンパウロ

        'europe-west1',  # ベルギー
        'europe-west2',  # ロンドン
        'europe-west3',  # フランクフルト
        'europe-west4',  # オランダ
        'europe-north1',  # フィンランド

        'asia-south1',  # ムンバイ
        'asia-southeast1',  # シンガポール
        'asia-east1',  # 台湾
        'asia-east2',  # 香港
        'asia-northeast1',  # 東京
        'australia-southeast1',  # シドニー
    ]
    location: str

    def __post_init__(self):
        if not isinstance(self.location, str):
            raise ValueError(f'location must be a string, expect: {type(self.location)}')

        if self.location not in self.AVAILABLE_LOCATIONS:
            raise ValueError(f'Invalid value of {self.location} is not available locations.')


@dataclasses.dataclass(frozen=True)
class Configuration:
    google_cloud_project: GoogleCloudProjectID
    google_cloud_location: GoogleCloudLocation