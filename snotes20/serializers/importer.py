from rest_framework.serializers import ModelSerializer, Field

from snotes20.models import ImporterLog, ImporterDatasourceLog, ImporterJobLog


class ImporterJobLogSerializer(ModelSerializer):
    runtime = Field()

    class Meta:
        fields = ('starttime', 'endtime', 'runtime', 'name', 'succeeded', 'error', 'created', 'deleted', 'skipped', 'updated')
        model = ImporterJobLog


class ImporterDatasourceLogSerializer(ModelSerializer):
    jobs = ImporterJobLogSerializer(many=True)
    runtime = Field()
    succeeded = Field()

    class Meta:
        fields = ('starttime', 'endtime', 'runtime', 'source', 'succeeded', 'jobs')
        model = ImporterDatasourceLog


class ImporterLogSerializer(ModelSerializer):
    sources = ImporterDatasourceLogSerializer(many=True)
    runtime = Field()
    succeeded = Field()

    class Meta:
        fields = ('starttime', 'endtime', 'runtime', 'succeeded', 'sources')
        model = ImporterLog
        depth = 3
