from sawtooth_sdk.processor.exceptions import InvalidTransaction


def handle_empty_asset_creation(create_asset,header,state):

    state.set_empty_asset(
        public_key = header.signer_public_key,
        child_public_key=create_asset.child_public_key,
        child_key_index=create_asset.child_key_index,
        is_empty_asset=create_asset.is_empty_asset
    )