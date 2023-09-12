import kfp.dsl as dsl
import kfp.components as comp
import kubernetes
node_affinity = kubernetes.client.models.v1_affinity.V1Affinity(
    node_affinity=kubernetes.client.V1NodeAffinity(
        required_during_scheduling_ignored_during_execution=kubernetes.client.V1NodeSelector(
            node_selector_terms=[kubernetes.client.V1NodeSelectorTerm(
                match_expressions=[kubernetes.client.V1NodeSelectorRequirement(
                    key='kubernetes.io/hostname',
                    operator='In',
                    values=['node1'])])])))

# copy_to_pvc_op = comp.load_component_from_file('copy_to_pvc.yaml')
# run_from_pvc_op = comp.load_component_from_file('run_from_pvc.yaml')

@dsl.pipeline(
    name='copy-and-run-files-pipeline',
    description='Copy and run files from node1 to node2'
)
def copy_and_run_files_pipeline():
    # Step 1: Define a PVC on node1
    vop = dsl.VolumeOp(
        name="connect-pvc",
        resource_name="jetson-pv-claim",
        storage_class="hostpath",
        modes=dsl.VOLUME_MODE_RWO,
        size="2Gi",
        generate_unique_name=True,#False,
        action='create',#'apply',
        ).add_affinity(node_affinity)
    
    vop.enable_caching = False

    # Step 3: Define a container to run files from PVC on node2
    run_from_pvc = dsl.ContainerOp(
        name='run-from-pvc',
        image='lachlanevenson/k8s-kubectl',  # Use an appropriate image
        command=['sh', '-c'],
        arguments=[
            'kubectl apply -f /root/data/cronjob.yaml'
        ],
        pvolumes={'/root/data': vop.volume}
    )

    run_from_pvc.enable_caching = False
    # copy_to_pvc = copy_to_pvc_op().add_pvolumes(pvolumes={"/mnt": vop.volume}).add_node_selector_constraint(label_name="key", value="master")
    # run_from_pvc = run_from_pvc_op().add_pvolumes(pvolumes={"/mnt": vop.volume}).add_node_selector_constraint(label_name="key", value="master")

    # Set run_from_volume to run after copy_to_volume
    # run_from_pvc.after(copy_to_pvc)

if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(copy_and_run_files_pipeline, 'test1-pipeline.yaml')

